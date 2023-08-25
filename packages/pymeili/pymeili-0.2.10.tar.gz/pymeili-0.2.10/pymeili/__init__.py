#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymeili.beautifyplot import (
    initplot,
    colorlist,
    cmaplist,
    getBARHNO,
    getBARNO,
    getHISTNO,
    getPLOTNO,
    getSCATTERNO,
    title, lefttitle, righttitle,
    scatter, plot, bar, hist, hist2d, pie, barh, table,
    contour, contourf, colorbar, polar,
    xlabel, ylabel, xticks, yticks, xyticks, ticksall,
    xlim, ylim, xylim, xscale, yscale, xlog, ylog,
    grid, spines, legend, hidespines, xaxisposition, yaxisposition,
    axhline, axvline, text, labeltext, annotate,
    fill_between, fill_betweenx,
    pause, normalize, slider, set_xydata,
    figsize, show, clf, close, figure, savefig,
    imread, imshow, imsave,
    
)

from pymeili.beautifyterminal import (
    fg, bg, DEFAULT,
    bprint, inspectfg, inspectbg,
)

__version__: str = '0.2.10'
