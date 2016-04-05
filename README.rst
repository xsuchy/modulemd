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
        components/packages:
                Optional.  A list of packages defining the module.  These should
                typically be autoinstalled when the module is enabled.  The list
                may contain objects with specific package constraints as well as
                simple package names.  These are the final package names.  Note
                other packages created from the source package, such as subpackages or
                debuginfo, as well as source packages, are also included in the module.
                However, they're not meant to be autoinstalled.
        components/packages/names:
                A list of packages to which the additional constraints apply.
                If no constraints are defined, objects with only the names property
                have the equal meaning as simple strings in components/packages.
        components/packages/arch:
                Optional. A list of architectures these packages should be available on.
                By default, all available architectures are available.
        components/dependencies:
                Control whether the module's components' dependencies should be
                included in the module or not.  True for dependency inclusion, false
                otherwise.
