metadata.json:
        A simple metadata template that should be a part of an RPM repository.
        It currently doesn't contain a link to the repository itself as the
        client already knows it anyway.  It doesn't contain a list of available
        components either, for similar reasons.

        The format should be mostly self-explanatory but just to be clear.

        version:
                Metadata format version.
        data:
                The main metadata structure.
        data/name:
                The module name.
        data/version:
                Module version.
                Currently suggested format is the version of the main module
                component plus the module's version, separated by a hyphen.
        data/license:
                Licenses details for the module.
        data/license/module:
                The license of the module itself.  This typically includes
                SPEC files, custom patches, the metadata file and similar.
        data/license/content:
                The license of the module content, i.e. RPMs.
        data/requires:
                A dictionary of the module's dependencies, with keys being
                the required modules' names and the values the minimum required
                versions of these.
        data/references:
                Optional.  Links to the upstream resources.
        data/references/community:
                Optional.  Upstream community website.
        data/references/documentation:
                Optional.  Upstream documentation.
        data/references/tracker:
                Optional.  Upstream release issue tracker.
        components:
                Optional.  Extra data for module components.
        components/install:
                Optional.  Lists module components that should be installed when
                the module is activated.
        components/install/type:
                Package type of the components, for example "rpm".
        components/install/packages:
                List of packages of the given type that should be installed.
