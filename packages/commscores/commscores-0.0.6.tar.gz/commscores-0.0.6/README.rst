Quantifying microbial interactions within microbial communities
________________________________________________________________________

|PyPI version| |Downloads| |License|

.. |Supported Python Versions| image:: https://img.shields.io/pypi/pyversions/commscores
   :target: https://pypi.org/project/commscores/
   :alt: Python versions

.. |PyPI version| image:: https://img.shields.io/pypi/v/modelseedpy.svg?logo=PyPI&logoColor=brightgreen
   :target: https://pypi.org/project/commscores/
   :alt: PyPI version

.. |Actions Status| image:: https://github.com/freiburgermsu/modelseedpy/workflows/Test%20modelseedpy/badge.svg
   :target: https://github.com/freiburgermsu/commscores/actions
   :alt: Actions Status

.. |License| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License

.. |Downloads| image:: https://pepy.tech/badge/commscores
   :target: https://pepy.tech/project/commscores
   :alt: Downloads

Microbial communities predicate most biological systems on Earth, yet the interaction dynamics between community members remains opaque. Quantitative metrics offer a means of isolating these complex, multi-dimensional, interactions into single biological dimensions; although, several ostensibly important biological dimensions evade existing metrics and extant metrics have moreover not be consolidated into a single operable package. We therefore developed CommScores as a comprehensive package for quantifying microbial interaction dimensions within a microbial community, and thereby elucidating the dynamics that govern the given community. CommScores leverages `ModelSEEDpy <https://github.com/ModelSEED/ModelSEEDpy>`_ and `COBRApy <https://github.com/opencobra/cobrapy>`_ packages for metabolic modeling, and the `COBRA-KBase <https://github.com/fliu/cobrakbase>`_ package for acquiring genomic information from KBase. CommScores should accelerate fundamental discoveries in microbial ecology and the rational design of microbial communities for diverse applications in medicine, ecology, and industry.

.. note::

   This project is under active development, and may be subject to losing back-compatibility.

----------------------
Installation
----------------------

CommScores and all of its dependencies should automatically install when it is installed from PyPI::

 pip install commscores
