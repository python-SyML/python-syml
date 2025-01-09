import streamlit as st

from syml.interract.page_class import BasePageElement


class Homepage(BasePageElement):
    def __init__(self) -> None:
        super().__init__()

    def setup(self):
        pass

    def introduction(self):
        st.logo("../python-syml/docs/source/img/narrow_banner.png", size="large")
        st.image("../python-syml/docs/source/img/narrow_banner.png")
        st.title("SyML Library :brain:")

        st.markdown("""
                    **Welcome to the SyML Library !**

                    ## Introduction

                    Thank you for dowloading SyML. Let us explain how it works.
                    SyML is a python library that provides several NLP, ML and xAI services encapsulated within a nice UI.
                    SyML aims to make data preparation, ML training and xAI usage the simplest possible.

                    On this page, you'll find explanations about each module of SyML and how to use them.
                    """)

        st.divider()

        st.markdown("""
                    ## Our Tools
                    You'll find below a small presentation of all our tools available (or soon available!) that will make your life
                    only easier and better.

                    ### I. Slide into my DMs (*Data Mining Module*)

                    The Data Mining Modules are a suite of pages on which you will be able to study, clean and improve your raw data
                    to then use it for ML purposes.

                    #### I.A. The 3D Module

                    The *:red[Data Discovery Dashboard]*, also called the "**:red[3D]**" module, aims to help you discover your raw data. You'll get
                    a better sense of its quality, what contains each field, the type of the data, and many other relevant information.

                    #### I.B. Our bff, QIA

                    Then you'll be able to leverage **:blue[QIA]**, the *:blue[Quality Improvement Assistant]*, to improve your data quality, coverage and uniformity.
                    Using NLP, outlier detection, data augmentation and other useful techniques, you will boost your data quality and coverage making your data
                    ready for the next stage !
                    """)
