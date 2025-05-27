# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# --------------------------------------------------------------------------------------------

# Use the current module's name to derive the path, making it independent of repo name
current_module = __name__  # "tasqsym_samples_more.library.library"
path = ".".join(current_module.split(".")[:-1]) + "."  # "tasqsym_samples_more.library."

library = {

    "action": {
        "decoder": path + "node.node.NodeDecoder",
        "src":     path + "node.node.Node",
        "src_configs": {"interruptible": True}
    },

}