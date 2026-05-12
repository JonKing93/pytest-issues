Contributing
============

Feedback
--------
We welcome feedback! To ask a question, report a bug, or suggest a feature, please open a new thread on our `issue tracker`_.


Contributing Code
-----------------
Please read this guide if you plan to contribute code.

Git Workflow
++++++++++++
You should use a `forking workflow`_ to contribute to pytest-issues. In brief, this means you should make a fork of the upstream repository, create a feature branch on your fork, and then submit pull requests from your feature branch to the main branch of the upstream.

Installation
++++++++++++
We use `uv`_ to manage the development ecosystem, and you can use uv to implement a developer installation.

1. `Install uv`_
2. Clone the repository
3. Navigate to the root of the cloned project. For example: ``cd path/to/pytest-issues``
4. Run ``uvx --from poethepoet poe setup``

This will install ``pytest-issues`` along with a number of developer tools, and will also set up various pre-commit hooks.

Scripts
+++++++
We use `poethepoet`_ to implement various commonly-used developer scripts. Run ``poe`` at the command line for an overview of available scripts.



.. _poethepoet: https://poethepoet.natn.io/index.html

.. _Install uv: https://docs.astral.sh/uv/getting-started/installation/

.. _uv: https://docs.astral.sh/uv/

.. _issue tracker: https://github.com/JonKing93/pytest-issues/issues

.. _forking workflow: https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html
