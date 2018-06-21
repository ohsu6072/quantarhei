"""

    Autogenerated by ghenerate script, part of Quantarhei
    http://github.com/tmancal74/quantarhei
    Tomas Mancal, tmancal74@gmai.com

    Generated on: 2018-06-11 09:20:58

    Edit the functions below to give them desired functionality.
    In present version of `ghenerate`, no edits or replacements
    are perfomed in the feature file text.

"""
import numpy

from behave import given
from behave import when
from behave import then

import quantarhei as qr
from quantarhei.spectroscopy.twod2 import _ptypes, _processes, _signals


def _spectrum(a, b):
    
    def func(x, y, a, b):
    
        Delta = b
        #omega = 2.0*3.14159/20.0 
        
        data = numpy.zeros((len(x), len(y)))
        
        for i_x in range(len(x)):
                data[i_x, :] = a*numpy.exp(-(x[i_x]/Delta)**2)* \
                                 numpy.exp(-(y/Delta)**2)
                data[i_x, :] -= (a/2.0)*numpy.exp(-(x[i_x]/Delta)**2)* \
                                 numpy.exp(-((y-Delta)/Delta)**2)
        
        return data

    xrange = qr.FrequencyAxis(-50.0, 100, 1.0)
    yrange = qr.FrequencyAxis(-50.0, 100, 1.0)
    
    data = func(xrange.data, yrange.data, a, b)
    
    return (xrange, yrange, data)


#
# Given ...
#
@given('that I have data corresponding to individual Liouville pathways in 2D spectrum')
def step_given_1(context):
    """

        Given that I have data corresponding to individual liouville pathways in 2D spectrum

    """
    
    data_list = []
    para_list = [[1.0, 10.0], [2.0, 20.0], [0.5, 12.0],
                 [0.1, 16.0], [0.2, 8.9], [0.3, 9.0]]
    types = ["R1fs", "R2g", "R3g", "R3g", "R1fs", "R2g"]
    tags  = ["r1f1", "r2g1", "r3g1", "r3g2", "r1f2", "r2g2"]


    for pars in para_list:
        data_list.append(_spectrum(pars[0], pars[1]))
        
        
    context.data_list = data_list
    context.types = types
    context.tags = tags
    


#
# When ...
#
@when('I create a new TwoDSpectrum object')
def step_when_2(context):
    """

        When I create a new TwoDSpectrum object

    """
    context.twod = qr.TwoDSpectrum()


#
# Then ...
#
@then('I can save 2D data using type and tag')
def step_then_3(context):
    """

        Then I can save 2D data using type and tag

    """
    twod = context.twod
    
    data_list = context.data_list
    types = context.types
    tags = context.tags
    
    k_l = 0
    for (x, y, data) in data_list:
        tpp = types[k_l]
        tag = tags[k_l]
        
        if (k_l == 0):
            twod.set_axis_1(x)
            twod.set_axis_3(y)
        twod._add_data(data, resolution="pathways", dtype=tpp, tag=tag)
        
        numpy.testing.assert_allclose(twod._d__data[tpp][tag], data)
        
        k_l += 1
        


#
# And ...
#
@then('I can retrieve spectra by type and tag')
def step_then_4(context):
    """

        And I can retrieve spectra by type and tag

    """
    twod = context.twod
    twod.set_resolution("pathways")
    
    data_list = context.data_list
    types = context.types
    tags = context.tags
    
    k_l = 0
    for (x, y, data) in data_list:
        tpp = types[k_l]
        tag = tags[k_l]
        
        twod.set_data_flag([tpp, tag])
        
        retrieved_data = twod.d__data 
        
        numpy.testing.assert_allclose(retrieved_data, data)
        k_l += 1


def _get_tag_of_type(typ, tags):
    """Selects all tags of pathways of a give tag
    
    """
    return_tags = []
    for tag in tags:
        if tag[0] == typ:
            return_tags.append(tag)
    return return_tags


def _sum_pathways_to_types(twod, type):
    
    tags = twod.get_all_tags()
    
    if type in _ptypes:
        tags_of_type = _get_tag_of_type(type, tags)

        dsum = numpy.zeros((twod.xaxis.length, twod.yaxis.length),
                           dtype=qr.COMPLEX)
        for pair in tags_of_type:
            twod.set_data_flag(pair)
            try:
                data = twod.d__data
                dsum += data
            except:
                pass

    return dsum


def _sum_pathways_to_process(twod, process):

    types = _processes[process]
    dsum = numpy.zeros((twod.xaxis.length, twod.yaxis.length),
                       dtype=qr.COMPLEX)   
    for typ in types:
        #twod.set_data_flag(typ)
        #data = twod.d__data
        data = _sum_pathways_to_types(twod, typ)
        if data is not None:
            dsum += data
            
    return dsum


def _sum_pathways_to_signal(twod, signal):
    
    types = _signals[signal]
    dsum = numpy.zeros((twod.xaxis.length, twod.yaxis.length),
                       dtype=qr.COMPLEX)   
    for typ in types:
        #twod.set_data_flag(typ)
        #data = twod.d__data
        data = _sum_pathways_to_types(twod, typ)
        if data is not None:
            dsum += data

    return dsum


def _sum_pathways_to_total(twod):

    dsum = numpy.zeros((twod.xaxis.length, twod.yaxis.length),
                       dtype=qr.COMPLEX)    
    for signal in _signals:
        data = _sum_pathways_to_signal(twod, signal)
        if data is not None:
            dsum += data
            
    return dsum


def _sum_types_to_process(twod, process):

    types = _processes[process]
    dsum = numpy.zeros((twod.xaxis.length, twod.yaxis.length),
                       dtype=qr.COMPLEX)   
    for typ in types:
        try:
            data = twod._d__data[typ]
        except:
            data = None
            
        if data is not None:
            dsum += data
            
    return dsum


def _sum_types_to_signal(twod, signal):

    types = _signals[signal]
    dsum = numpy.zeros((twod.xaxis.length, twod.yaxis.length),
                       dtype=qr.COMPLEX)   
    for typ in types:
        try:
            data = twod._d__data[typ]
        except:
            data = None
            
        if data is not None:
            dsum += data
            
    return dsum


def _sum_types_to_total(twod):

    dsum = numpy.zeros((twod.xaxis.length, twod.yaxis.length),
                       dtype=qr.COMPLEX)   
    for typ in _ptypes:
        try:
            data = twod._d__data[typ]
        except:
            data = None
            
        if data is not None:
            dsum += data
            
    return dsum


def _sum_processes_to_total(twod):

    dsum = numpy.zeros((twod.xaxis.length, twod.yaxis.length),
                       dtype=qr.COMPLEX) 
    for process in _processes:
        try:
            data = twod._d__data[process]
        except:
            data = None
            
        if data is not None:
            dsum += data
            
    return dsum


def _sum_signals_to_total(twod):

    dsum = numpy.zeros((twod.xaxis.length, twod.yaxis.length),
                       dtype=qr.COMPLEX) 
    for signal in _signals:
        try:
            data = twod._d__data[signal]
        except:
            data = None
            
        if data is not None:
            dsum += data
            
    return dsum

#
# And ...
#
@then('I can retrieve sum of spectra of a given type {type}')
def step_then_5(context, type):
    """

        And I can retrieve sum of spectra of a given type {type}

    """


    # first we get data for comparison
    twod = context.twod
    
    res = twod.get_resolution()
    
    if res == "pathways":
        dsum = _sum_pathways_to_types(twod, type)
    elif res == "types":
        dsum = twod._d__data[type]
    
    # here we test it without first changing the resolution
    twod.set_data_flag(type)
    
    retrieved_data = twod.d__data
    
    numpy.testing.assert_allclose(retrieved_data, dsum, atol=1.0e-5)
    

#
# And ...
#
@then('I can retrieve sum of spectra of a given process {process}')
def step_then_6(context, process):
    """

        And I can retrieve sum of spectra of a given process {process}

    """
    # first we get data for comparison
    twod = context.twod
    
    res = twod.get_resolution()
    
    if res == "pathways":
        dsum = _sum_pathways_to_process(twod, process)
    elif res == "types":
        dsum = _sum_types_to_process(twod, process)
    elif res == "processes":
        dsum = twod._d__data[process]

#    twod.set_resolution("processes")
    twod.set_data_flag(process)
    
    retrieved_data = twod.d__data
    
    numpy.testing.assert_allclose(retrieved_data, dsum)    



#
# And ...
#
@then('I can retrieve sum of spectra of a given signal {signal}')
def step_then_7(context, signal):
    """

        And I can retrieve sum of spectra of a given signal {signal}

    """
    # first we get data for comparison
    twod = context.twod
    
    res = twod.get_resolution()
    
    if res == "pathways":
        dsum = _sum_pathways_to_signal(twod, signal)
    elif res == "types":
        dsum = _sum_types_to_signal(twod, signal)
    elif res == "signals":
        dsum = twod._d__data[signal]
        
#    twod.set_resolution("processes")
    twod.set_data_flag(signal)
    
    retrieved_data = twod.d__data
    
    numpy.testing.assert_allclose(retrieved_data, dsum)


#
# And ...
#
@then('I can retrieve total spectrum')
def step_then_8(context):
    """

        And I can retrieve total spectrum

    """
    # first we get data for comparison
    twod = context.twod
    
    res = twod.get_resolution()
    
    if res == "pathways":
        dsum = _sum_pathways_to_total(twod)
    elif res == "types":
        dsum = _sum_types_to_total(twod)
    elif res == "processes":
        dsum = _sum_processes_to_total(twod)
    elif res == "signals":
        dsum = _sum_signals_to_total(twod)
    elif res == "off":
        #dsum = twod._d__data["total"]

        data_list = context.data_list    
        k_l = 0
        for (x, y, data) in data_list:
            if k_l == 0:
                dsum = data.copy()
            else:
                dsum += data        
            k_l += 1

    else:
        raise Exception("Unknow storage resolution: "+res)
    
#    twod.set_resolution("processes")
    twod.set_data_flag("total")
    
    retrieved_data = twod.d__data
    
    numpy.testing.assert_allclose(retrieved_data, dsum)


#
# And ...
#
@given('I create a new TwoDSpectrum object')
def step_given_9(context):
    """

        And I create a new TwoDSpectrum object

    """
    context.twod = qr.TwoDSpectrum()


#
# And ...
#
@given('I save 2D data using type and tag')
def step_given_10(context):
    """

        And I save 2D data using type and tag

    """
    twod = context.twod
    
    data_list = context.data_list
    types = context.types
    tags = context.tags
    
    k_l = 0
    for (x, y, data) in data_list:
        tpp = types[k_l]
        tag = tags[k_l]
        
        if (k_l == 0):
            twod.set_axis_1(x)
            twod.set_axis_3(y)
        twod._add_data(data, resolution="pathways", dtype=tpp, tag=tag)
        
        numpy.testing.assert_allclose(twod._d__data[tpp][tag], data)
        
        k_l += 1
    

#
# When ...
#
@when('I convert the storage mode into the one storing only types of pathways')
def step_when_11(context):
    """

        When I convert the storage mode into the one storing only types of pathways

    """
    twod = context.twod
    twod.set_resolution("types")
    

#
# When ...
#
@when('I convert the storage mode into the one storing spectra of processes')
def step_when_12(context):
    """

        When I convert the storage mode into the one storing spectra of processes

    """
    twod = context.twod
    twod.set_resolution("processes")


#
# But ...
#
@then('when I try to retrieve signal {signal} I get an exception')
def step_then_13(context, signal):
    """

        But when I try to retrieve signal {signal} I get an exception

    """
    twod = context.twod
    
    twod.set_data_flag(signal)
    
    got_exception = False
    try:
        twod.d__data
    except:
        got_exception = True 
    
    assert got_exception


#
# When ...
#
@when('I convert the storage mode into the one storing rephasing and non-rephasing signals')
def step_when_14(context):
    """

        When I convert the storage mode into the one storing rephasing and non-rephasing signals

    """
    twod = context.twod
    twod.set_resolution("signals")

#
# But ...
#
@then('when I try to retrieve process {process} I get an exception')
def step_then_15(context, process):
    """

        But when I try to retrieve process {process} I get an exception

    """
    pass


#
# When ...
#
@when('I convert the storage mode into the storing total spectrum')
def step_when_16(context):
    """

        When I convert the storage mode into the storing total spectrum

    """
    twod = context.twod
    twod.set_resolution("off")


#
# Given ...
#
@given('that I have data corresponding to Liouville pathway types')
def step_given_17(context):
    """

        Given that I have data corresponding to Liouville pathway types

    """
    data_list = []
    para_list = [[1.0, 10.0], [2.0, 20.0], [0.5, 12.0],
                 [0.1, 16.0], [0.2, 8.9], [0.3, 9.0]]
    types = ["R1fs", "R2g", "R3g", "R3g", "R1fs", "R2g"]


    for pars in para_list:
        data_list.append(_spectrum(pars[0], pars[1]))
        
        
    context.data_list = data_list
    context.types = types


#
# And ...
#
@given('I save 2D data using type information')
def step_given_18(context):
    """

        And I save 2D data using type information

    """
    twod = context.twod
    twod.set_resolution("types")
    data_list = context.data_list
    types = context.types
    
    k_l = 0
    for (x, y, data) in data_list:
        tpp = types[k_l]
        
        if (k_l == 0):
            twod.set_axis_1(x)
            twod.set_axis_3(y)
        twod._add_data(data, dtype=tpp)
        
        #numpy.testing.assert_allclose(twod._d__data[tpp], data)
        
        k_l += 1


#
# When ...
#
@when('I convert the storage mode into the one storing spectra of rephasing and non-rephasing signals')
def step_when_19(context):
    """

        When I convert the storage mode into the one storing spectra of rephasing and non-rephasing signals

    """
    twod = context.twod
    twod.set_resolution("signals")


#
# And ...
#
@then('when I try to retrieve pathways I get an exception')
def step_then_20(context):
    """

        And when I try to retrieve pathways I get an exception

    """
    twod = context.twod
    twod.set_data_flag(["R1fs", "path1"])
    
    got_exception = False
    
    try:
        twod.d__data
    except:
        got_exception = True
        
    assert got_exception
    
    
#
# Given ...
#
@given('that I have data corresponding to signal types')
def step_given_21(context):
    """

        Given that I have data corresponding to signal types

    """
    data_list = []
    para_list = [[1.0, 10.0], [2.0, 20.0], [0.5, 12.0],
                 [0.1, 16.0], [0.2, 8.9], [0.3, 9.0]]
    types = ["REPH", "REPH", "REPH", "REPH", "NONR", "NONR"]


    for pars in para_list:
        data_list.append(_spectrum(pars[0], pars[1]))
        
        
    context.data_list = data_list
    context.types = types

#
# And ...
#
@given('I save 2D data using signal types')
def step_given_22(context):
    """

        And I save 2D data using signal types

    """
    twod = context.twod
    twod.set_resolution("signals")
    data_list = context.data_list
    types = context.types
    
    k_l = 0
    for (x, y, data) in data_list:
        tpp = types[k_l]
        
        if (k_l == 0):
            twod.set_axis_1(x)
            twod.set_axis_3(y)
        twod._add_data(data, dtype=tpp)
        
        #numpy.testing.assert_allclose(twod._d__data[tpp], data)
        
        k_l += 1


#
# And ...
#
@then('when I try to retrieve types of spectra I get an exception')
def step_then_23(context):
    """

        And when I try to retrieve types of spectra I get an exception

    """
    twod = context.twod
    twod.set_data_flag("R1fs")
    got_exception = False
    try:
        twod.d__data
    except:
        got_exception = True
    
    assert got_exception

    
#
# Given ...
#
@given('that I have data corresponding to processes')
def step_given_24(context):
    """

        Given that I have data corresponding to processes

    """
    data_list = []
    para_list = [[1.0, 10.0], [2.0, 20.0], [0.5, 12.0],
                 [0.1, 16.0], [0.2, 8.9], [0.3, 9.0]]
    types = ["GSB", "ESA", "SE", "GSB", "SE", "ESA"]

    for pars in para_list:
        data_list.append(_spectrum(pars[0], pars[1]))
        
        
    context.data_list = data_list
    context.types = types

#
# And ...
#
@given('I save 2D data using processes')
def step_given_25(context):
    """

        And I save 2D data using processes

    """
    twod = context.twod
    twod.set_resolution("processes")
    data_list = context.data_list
    types = context.types
    
    k_l = 0
    for (x, y, data) in data_list:
        tpp = types[k_l]
        
        if (k_l == 0):
            twod.set_axis_1(x)
            twod.set_axis_3(y)
        twod._add_data(data, dtype=tpp)
        
        #numpy.testing.assert_allclose(twod._d__data[tpp], data)
        
        k_l += 1


#
# Given ...
#
@given('that I have data corresponding to total spectrum')
def step_given_26(context):
    """

        Given that I have data corresponding to total spectrum

    """
    data_list = []
    para_list = [[1.0, 10.0], [2.0, 20.0], [0.5, 12.0],
                 [0.1, 16.0], [0.2, 8.9], [0.3, 9.0]]
    types = ["GSB", "ESA", "SE", "GSB", "SE", "ESA"]

    for pars in para_list:
        data_list.append(_spectrum(pars[0], pars[1]))
        
        
    context.data_list = data_list
    context.types = types


#
# When ...
#
@when('I save 2D data of the total spectrum')
def step_when_27(context):
    """

        When I save 2D data of the total spectrum

    """
    twod = context.twod
    twod.set_resolution("off")
    data_list = context.data_list
    
    k_l = 0
    for (x, y, data) in data_list:        
        if (k_l == 0):
            totd = data.copy()
            twod.set_axis_1(x)
            twod.set_axis_3(y)            
        else:
            totd += data
        k_l += 1

    twod._add_data(totd, dtype="total")


#
# And ...
#
@given('I trim the data to half the length of the axes')
def step_given_28(context):
    """

        And I trim the data to half the length of the axes

    """
    twod = context.twod
    
    minx = twod.xaxis.min
    maxx = twod.xaxis.max
    miny = twod.yaxis.min
    maxy = twod.yaxis.max
    
    xcentr = (minx+maxx)/2.0
    xwidth = maxx-xcentr
    minx = xcentr - xwidth/2.0
    maxx = xcentr + xwidth/2.0
    
    ycentr = (miny+maxy)/2.0
    ywidth = maxy-ycentr
    miny = ycentr - ywidth/2.0
    maxy = ycentr + ywidth/2.0
    
    twod.set_data_flag("total")
    shp = twod.d__data.shape
    context.shape = shp
    
    twod.trim_to(window=[minx, maxx, miny, maxy])


#
# Then ...
#
@then('I can retrieve total spectrum with half the length of the axes')
def step_then_29(context):
    """

        Then I can retrieve total spectrum with half the length of the axes

    """
    twod = context.twod
    
    twod.set_data_flag("total")
    tot_spect = twod.d__data
    
    shp_half = tot_spect.shape
    shp = context.shape
    
    assert (shp_half[0] < shp[0]) and (shp_half[1] < shp[1]) 


#
# And ...
#
@given('I convert the storage mode into {storage_mode}')
def step_given_30(context, storage_mode):
    """

        And I convert the storage mode into {storage_mode}

    """
    twod = context.twod
    
    twod.set_resolution(storage_mode)


#
# When ...
#
@when('I devide the spectrum by number {number}')
def step_when_31(context, number):
    """

        When I devide the spectrum by number {number}

    """
    nr_f = float(number)
    nr_f_inv = 1.0/nr_f
    try:
        nr_i = int(number)
    except ValueError:
        nr_i = 1
    nr_i_inv = 1.0/nr_i
    
    twod = context.twod
    twod.devide_by(nr_i)
    twod.devide_by(nr_i_inv)
    twod.devide_by(nr_f)
    twod.devide_by(nr_f_inv)


#
# Then ...
#
@then('I can retrieve total spectrum at a point [{px}, {py}]')
def step_then_32(context, px, py):
    """

        Then I can retrieve total spectrum at a point [{px}, {py}]

    """
    twod = context.twod
    pxn = float(px)
    pyn = float(py)
    twod.set_data_flag("total")
    val = twod.get_value_at(pxn, pyn)
    
    
    