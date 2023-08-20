# ==============================================================================
# Copyright (c)  2018 VerifAI All Rights Reserved.
#
# ==============================================================================


from setuptools import setup, find_packages


setup(name='multillm',
      version='0.907',
      description='VerifAI MultiLLM: A module to invoke multiple LLMs concurrently and rank their results',
      packages=["multillm","multillm/models"],
      author_name = "VerifAI Inc",
    author_email="hello@verifai.ai" ,
     install_requires=[
          'openai',
          'vertexai'
      ],
     scripts=['multillm/bin/multillm'],
 include_package_data=True,
 #     entry_points={
 #         'console_scripts': [
#              'multillm = multillm.example:main(args)'
#          ]},
      data_files = [ ("", ["multillm/requirements.txt"]),("", ["multillm/LICENSE"]), ("",["multillm/README.md","multillm/config.json"])]
      )
      
