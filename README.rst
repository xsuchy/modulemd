Module metadata definitions
===========================

This repository contains simple module metadata templates.

metadata.yaml:
        This file serves two roles -- it is the input for tools generating the
        actual module (such as pungi-modularization) and it is also present in
        the resulting repository, available to its consumers (such as
        fm-metadata-service).  For practical reasons, it is written in YAML.
        See comments in the template for details.
