import sys
import onnx
from tabulate import tabulate
import onnx_graphsurgeon as gs
from onnx_graphsurgeon.logger.logger import G_LOGGER

from loguru import logger
from .utils.font import GREEN, WHITE

class OnnxSlim():
    def __init__(self, model, log_level=1):
        self.model = onnx.load(model)
        self.float_op_info = self.summarize(self.model)
        self.init_logging(log_level)

    def init_logging(self, log_level):
        logger.remove()
        if log_level == 0: # DEBUG
            logger.add(sys.stderr, level=G_LOGGER.DEBUG)
        elif log_level == 1: # INFO
            logger.add(sys.stderr, level=G_LOGGER.INFO)
        elif log_level == 2: # WARNING
            logger.add(sys.stderr, level=G_LOGGER.WARNING)
        elif log_level == 3: # ERROR
            logger.add(sys.stderr, level=G_LOGGER.ERROR)
        else:
            raise Exception("level must be 0, 1, 2 or 3")
        
        G_LOGGER.severity = G_LOGGER.ERROR
        
    def shape_infer(self):
        self.model = onnx.shape_inference.infer_shapes(self.model, strict_mode=False, data_prop=True)

    def slim(self):
        self.graph = gs.import_onnx(self.model).toposort()
        self.graph.fold_constants().cleanup().toposort()
        self.model = gs.export_onnx(self.graph)

    def summary(self):
        self.slimmed_op_info = self.summarize(self.model)
        final_op_info = []
        all_ops = set(list(self.float_op_info.keys()) + list(self.slimmed_op_info.keys()))
        sorted_ops = sorted(all_ops, key=lambda x: x[0])
        for op in sorted_ops:
            float_number = self.float_op_info.get(op, 0)
            slimmed_number = self.slimmed_op_info.get(op, 0)
            if float_number > slimmed_number:
                slimmed_number = GREEN+str(slimmed_number)+WHITE
            final_op_info.append([op, float_number, slimmed_number])
        
        logger.info(WHITE+"\n" + tabulate(final_op_info,headers=["OP_TYPE", "Original Model", "Slimmed Model"], tablefmt="pretty"))

    def summarize(self, model):
        op_type_counts = {}

        for node in model.graph.node:
            op_type = node.op_type
            if op_type in op_type_counts:
                op_type_counts[op_type] += 1
            else:
                op_type_counts[op_type] = 1

        return op_type_counts             

    def save(self, model_path):
        onnx.save(self.model, model_path)