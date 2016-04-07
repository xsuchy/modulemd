metadata.json:
        A simple metadata template that should be a part of an RPM repository.
        It currently doesn't contain a link to the repository itself as the
        client already knows it anyway.  It doesn't contain a list of available
        components either, for similar reasons.

        The format should be mostly self-explanatory but just to be clear.

        version:
                Metadata format version, an integer.
                This should only change when incompatible changes are introduced.
        data:
                The main metadata structure.
        data/name:
                The module name.
        data/version:
                Module version.
                Currently suggested format is the version of the main module
                component plus the module's version, separated by a hyphen.
                Much like the RPM's VR scheme.
        data/summary:
                A short summary of the module's purpose.
        data/description:
                A short description of the module.
        data/license:
                Licenses details for the module.
        data/license/module:
                The license of the module itself.  This typically includes
                SPEC files, custom patches, the metadata file and similar.
        data/license/content:
                The license of the module content, i.e. RPMs.
        data/buildrequires:
                A dictionary of the module's build dependencies, with keys being
                the required modules' names and the values the minimum required
                versions of these.
        data/requires:
                A dictionary of the module's runtime dependencies, with keys being
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
        components/packages:
                A list of objects representing the packages defining the module.
                These should only have one property with its value being an object
                with packaging constraints.  These packages should typically be
                autoinstalled when the module is enabled.
        components/packages/<pkgname>/arch:
                Optional. A list of architectures these packages should be available on.
                By default, all available architectures are available.
        components/dependencies:
                Control whether the module's components' dependencies should be
                included in the module or not.  True for dependency inclusion, false
                otherwise.
        components/fulltree:
                Control whether related packages such as debuginfo or unlisted
                subpackages should be included in the module as well.  These wouldn't
                be autoinstalled, just present.  True for inclusion, false otherwise.
