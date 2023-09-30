import pdal
from pdal import Pipeline

# def execute(json, return_array=False):
#     r = pdal.Pipeline(json)
#     r.execute()
#     if return_array:
#         return r.arrays
#     else:
#         pass

def readLAS(LAS_input):
    dict = {"type": "readers.las", "filename": LAS_input}
    pipeline = [dict]
    json = '{' + "'pipeline':" '{}'.format(pipeline) + '}'
    json = json.replace("'", '"')
    r = pdal.Pipeline(json)
    r.execute()    
#     LAS_array = execute(json, return_array=True)
    return r.arrays

class classifyGround():
    def __init__(self, method="use_return_number"):
        self.method = method
        if self.method=="use_return_number":
            self.dict = {"type":"filters.range", "limits":"returnnumber[1:1]"}
        else:
            self.dict = {}
    def execute(self, LAS_array):
        p = [self.dict]
        json = '{' + "'pipeline':" '{}'.format(p) + '}'
        json = json.replace("'", '"')
        pipe = Pipeline(json = json, arrays = LAS_array)
        pipe.execute()
        return pipe.arrays

class rasterize():
    def __init__(self, TIF_output, resolution):
        self.tif_out = TIF_output
        self.resolution = resolution
        self.dict = {"type": "writers.gdal",
             "filename": self.tif_out,
             "output_type":"idw",
             "gdaldriver":"GTiff",
             "resolution": self.resolution,
             "radius": 1}
    def execute(self, LAS_array):
        p = [self.dict]
        json = '{' + "'pipeline':" '{}'.format(p) + '}'
        json = json.replace("'", '"')
        pipe = Pipeline(json = json, arrays = LAS_array)
        pipe.execute()
        return pipe.arrays        
        
class assign():
    def __init__(self, assignment="Classification[:]=0"):
        self.type = "filters.assign"
        self.assignment =assignment
        self.dict = {
            "type": self.type,
            "assignment":self.assignment}
    def execute(self, LAS_array):
        p = [self.dict]
        json = '{' + "'pipeline':" '{}'.format(p) + '}'
        json = json.replace("'", '"')
        pipe = Pipeline(json = json, arrays = LAS_array)
        pipe.execute()
        return pipe.arrays 

class elm():
    def __init__(self):
        self.dict = {
            "type": "filters.elm"}
    def execute(self, LAS_array):
        p = [self.dict]
        json = '{' + "'pipeline':" '{}'.format(p) + '}'
        json = json.replace("'", '"')
        pipe = Pipeline(json = json, arrays = LAS_array)
        pipe.execute()
        return pipe.arrays 
    
class outlier():
    def __init__(self):
        self.dict = {
            "type": "filters.outlier"}
    def execute(self, LAS_array):
        p = [self.dict]
        json = '{' + "'pipeline':" '{}'.format(p) + '}'
        json = json.replace("'", '"')
        pipe = Pipeline(json = json, arrays = LAS_array)
        pipe.execute()
        return pipe.arrays     

class smrf():
    def __init__(self, ignore="Classification[7:7]", slope=.2, window=16, threshold=.45, scalar=1.2):
        self.ignore = ignore
        self.slope = slope
        self.window = window
        self.threshold = threshold
        self.scalar = scalar
        self.dict = {
           "type":"filters.smrf",
           "ignore":self.ignore,
           "slope":self.slope,
           "window":self.window,
           "threshold":self.threshold,
           "scalar":self.scalar}
    def execute(self, LAS_array):
        p = [self.dict]
        json = '{' + "'pipeline':" '{}'.format(p) + '}'
        json = json.replace("'", '"')
        pipe = Pipeline(json = json, arrays = LAS_array)
        pipe.execute()
        return pipe.arrays

class frange():
    def __init__(self, limits="Classification[2:2]"):
        self.classification = limits
        self.dict = {
            "type": "filters.range",
            "limits": self.limits}
    def execute(self, LAS_array):
        p = [self.dict]
        json = '{' + "'pipeline':" '{}'.format(p) + '}'
        json = json.replace("'", '"')
        pipe = Pipeline(json = json, arrays = LAS_array)
        pipe.execute()
        return pipe.arrays    

class make_pipeline():
    def __init__(self, list_of_functions):
        pipeline = []
        for f in list_of_functions:
            pipeline.append(f.dict)
        self.pipeline = pipeline
    def execute(self, LAS_array):
        p = self.pipeline
        json = '{' + "'pipeline':" '{}'.format(p) + '}'
        json = json.replace("'", '"')
        pipe = Pipeline(json = json, arrays = LAS_array)
        pipe.execute()
        return pipe.arrays

def createDSM(LAS_array, TIF_output, resolution=1):
    clf = classifyGround(method="use_return_number")
    rst = rasterize(TIF_output, resolution)
    pipe = make_pipeline([clf, rst])
    pipe.execute(LAS_array)

def createDTM(LAS_array, TIF_output, resolution=1):
    asn = assign()
    el = elm()
    out = outlier()
    smf = smrf()
    rst = rasterize(TIF_output, resolution)
    fr = frange()
    pipe = make_pipeline([asn, el, out, smf, rst, fr])
    pipe.execute()

def createCHM(LAS_array):
    x = createDSM(LAS_array)
    y = createDTM(LAS_array)
    return 3
