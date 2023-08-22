"""ChatSSM Streamlit Component."""


from collections import defaultdict
from uuid import uuid4

import streamlit as st

from openssm.core.ssm.rag_ssm import RAGSSM
from openssm import LlamaIndexSSM


class ChatSSMComponent:
    """ChatSSM Streamlit Component."""

    KNOWLEDGE_SRC_PARDIR_PATH_SESS_STATE_KEY: str = '_knowledge_src_pardir_path'
    KNOWLEDGE_SRC_FILE_PATHS_SESS_STATE_KEY: str = '_knowledge_src_file_paths'

    SSMS_SESS_STATE_KEY: str = '_ssm'

    SSM_CONVO_IDS_SESS_STATE_KEY: str = '_ssm_convo_id'
    SSM_INTROS_SESS_STATE_KEY: str = '_ssm_intro'

    SSM_CONVO_NEXTQ_SESS_STATE_KEY: str = '_ssm_nextq'
    SSM_CONVO_QBOX_SESS_STATE_KEY: str = '_ssm_qbox'

    def __init__(self, uuid: str = '', name: str = '', knowledge_src_pardir_path: str = ''):
        # initialize UUID & Name
        self.uuid: str = str(uuid) if uuid else str(uuid4())
        self.name: str = str(name) if name else self.uuid

        # initialize relevant Streamlit session state elements if necessary
        self._init_knowledge_src_pardir_path_sess_state()
        self._init_knowledge_src_file_paths_sess_state()

        self._init_ssms_sess_state()

        self._init_ssm_convo_ids_sess_state()
        self._init_ssm_intros_sess_state()

        # set Knowledge Source Parent Directory Path if given
        if knowledge_src_pardir_path:
            self.knowledge_src_pardir_path: str = knowledge_src_pardir_path
            # initilize SSM & load Knowledge Source
            self.ssm_load_knowledge()

    def _init_knowledge_src_pardir_path_sess_state(self):
        if self.KNOWLEDGE_SRC_PARDIR_PATH_SESS_STATE_KEY not in st.session_state:
            st.session_state[self.KNOWLEDGE_SRC_PARDIR_PATH_SESS_STATE_KEY]: defaultdict[str, str] = defaultdict(str)

    @property
    def knowledge_src_pardir_path(self) -> str:
        return st.session_state[self.KNOWLEDGE_SRC_PARDIR_PATH_SESS_STATE_KEY][self.uuid]

    @knowledge_src_pardir_path.setter
    def knowledge_src_pardir_path(self, knowledge_src_pardir_path: str, /):
        st.session_state[self.KNOWLEDGE_SRC_PARDIR_PATH_SESS_STATE_KEY][self.uuid]: str = knowledge_src_pardir_path

    def _init_knowledge_src_file_paths_sess_state(self):
        if self.KNOWLEDGE_SRC_FILE_PATHS_SESS_STATE_KEY not in st.session_state:
            st.session_state[self.KNOWLEDGE_SRC_FILE_PATHS_SESS_STATE_KEY]: defaultdict[str, set[str]] = defaultdict(set)

    def _init_ssms_sess_state(self):
        if self.SSMS_SESS_STATE_KEY not in st.session_state:
            st.session_state[self.SSMS_SESS_STATE_KEY]: defaultdict[str, RAGSSM] = defaultdict(LlamaIndexSSM)

    @property
    def ssm(self) -> RAGSSM:
        return st.session_state[self.SSMS_SESS_STATE_KEY][self.uuid]

    @ssm.setter
    def ssm(self, ssm: RAGSSM, /):
        st.session_state[self.SSMS_SESS_STATE_KEY][self.uuid]: RAGSSM = ssm

    def ssm_load_knowledge(self):
        if self.knowledge_src_pardir_path.startswith('s3://'):
            self.ssm.read_s3(self.knowledge_src_pardir_path)
        else:
            self.ssm.read_directory(self.knowledge_src_pardir_path)

    def _init_ssm_convo_ids_sess_state(self):
        if self.SSM_CONVO_IDS_SESS_STATE_KEY not in st.session_state:
            st.session_state[self.SSM_CONVO_IDS_SESS_STATE_KEY]: defaultdict[str, str] = defaultdict(lambda: str(uuid4()))

    @property
    def ssm_convo_id(self) -> str:
        return st.session_state[self.SSM_CONVO_IDS_SESS_STATE_KEY][self.uuid]

    def reset_ssm_convo_id(self):
        st.session_state[self.SSM_CONVO_IDS_SESS_STATE_KEY][self.uuid]: str = str(uuid4())

    def _init_ssm_intros_sess_state(self):
        if self.SSM_INTROS_SESS_STATE_KEY not in st.session_state:
            st.session_state[self.SSM_INTROS_SESS_STATE_KEY]: defaultdict[str, str] = defaultdict(str)

    def ssm_intro(self, refresh: bool = False) -> str:
        if refresh or (not st.session_state[self.SSM_INTROS_SESS_STATE_KEY][self.uuid]):
            self.reset_ssm_convo_id()

            st.session_state[self.SSM_INTROS_SESS_STATE_KEY][self.uuid]: str = \
                self.ssm.discuss(user_input=(('In 100 words, summarize your expertise '
                                              'after you have read the following documents: '
                                              '(do NOT restate these sources in your answer)\n') +  # noqa: W504
                                             '\n'.join([self.knowledge_src_pardir_path])),
                                 conversation_id=self.ssm_convo_id)['content']

            self.reset_ssm_convo_id()

        return st.session_state[self.SSM_INTROS_SESS_STATE_KEY][self.uuid]

    def ssm_discuss(self):
        def submit_question():
            # discuss if question box is not empty
            if (next_question := st.session_state[self.SSM_CONVO_QBOX_SESS_STATE_KEY].strip()):
                self.ssm.discuss(user_input=next_question, conversation_id=self.ssm_convo_id)

            # empty question box
            st.session_state[self.SSM_CONVO_QBOX_SESS_STATE_KEY]: str = ''

        st.text_area(label='Next Question', height=3,
                     key=self.SSM_CONVO_QBOX_SESS_STATE_KEY, on_change=submit_question)

        for msg in self.ssm.conversations.get(self.ssm_convo_id, []):
            st.write(f"{'__YOU__' if (msg['role'] == 'user') else '__SSM__'}: {msg['content']}")

    def run(self):
        """Run ChatSSM Streamlit Component on Streamlit app page."""
        st.subheader(f'__Small Specialist Model (SSM): {self.name}__')

        if knowledge_src_pardir_path := st.text_input(label='Knowledge Source Parent Directory Path (Local|S3|GCS|GDrive)',
                                                      value=self.knowledge_src_pardir_path,
                                                      max_chars=None,
                                                      key=None,
                                                      type='default',
                                                      help='Knowledge Source Parent Directory Path (Local|S3|GCS|GDrive)',
                                                      autocomplete=None,
                                                      on_change=None, args=None, kwargs=None,
                                                      placeholder=None,
                                                      disabled=False,
                                                      label_visibility='visible'):
            if to_reload := knowledge_src_pardir_path != self.knowledge_src_pardir_path:
                # set new Knowledge Source Parent Directory Path
                self.knowledge_src_pardir_path: str = knowledge_src_pardir_path
                # initilize SSM & load Knowledge Source
                self.ssm_load_knowledge()

            st.write(f'__MY SPECIALIZED EXPERTISE:__ {self.ssm_intro(refresh=to_reload)}')

            if st.button(label='Reset Discussion',
                         key=None,
                         on_click=None, args=None, kwargs=None,
                         type='secondary',
                         disabled=False,
                         use_container_width=False):
                self.reset_ssm_convo_id()

            self.ssm_discuss()
