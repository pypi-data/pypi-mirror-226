#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Exploratory Data Analysis Framework                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /d8analysis/__init__.py                                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/d8analysis                                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday May 26th 2023 11:59:46 pm                                                    #
# Modified   : Sunday August 20th 2023 07:30:01 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
# Data Package
# Generation
from d8analysis.data.generation import RVSDistribution  # noqa F402
from d8analysis.data.dataset import Dataset  # noqa F402

# Qualitative Package
# - Quantitative Package
# -- Descriptive Subpackage
from d8analysis.quantitative.descriptive.categorical import (  # noqa F402
    CategoricalStats,
)
from d8analysis.quantitative.descriptive.continuous import (  # noqa F402
    ContinuousStats,
)

# Inferential Subpackage
from d8analysis.quantitative.inferential.centrality.ttest import TTest, TTestResult  # noqa F402
from d8analysis.quantitative.inferential.distribution.kstest import (  # noqa F402
    KSTest,
    KSTestResult,
)
from d8analysis.quantitative.inferential.relational.chisquare import (  # noqa F402
    ChiSquareIndependenceResult,
    ChiSquareIndependenceTest,
)
from d8analysis.quantitative.inferential.relational.pearson import (  # noqa F402
    PearsonCorrelationResult,
    PearsonCorrelationTest,
)
from d8analysis.quantitative.inferential.relational.spearman import (  # noqa F402
    SpearmanCorrelationResult,
    SpearmanCorrelationTest,
)

# Visualization Package
# - Seaborn
from d8analysis.visual.seaborn.association import (  # noqa F402
    PairPlot,
    ScatterPlot,
    JointPlot,
    LinePlot,
)  # noqa F402
from d8analysis.visual.seaborn.distribution import (  # noqa F402
    Histogram,
    HistPDFPlot,
    ECDFPlot,
    KDEPlot,
    BoxPlot,
    ViolinPlot,
    PdfCdfPlot,
)
from d8analysis.visual.seaborn.centrality import Barplot  # noqa F402
from d8analysis.visual.seaborn.grid import GridPlot  # noqa F402
