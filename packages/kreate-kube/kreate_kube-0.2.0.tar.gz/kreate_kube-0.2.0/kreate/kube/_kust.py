import logging

from ..kore import Konfig
from ..kore import JinYamlKomponent
from .resource import Resource
from . import KubeApp
from . import other_templates
from . import patch_templates
from .patch import AddEgressLabelsPatch
from .patch import Patch

logger = logging.getLogger(__name__)


class KustApp(KubeApp):
    def __init__(self, konfig: Konfig):
        super().__init__(konfig)
        self.register_templates_from_konfig("patch_templates", Patch)

    def register_std_templates(self) -> None:
        super().register_std_templates()
        self.register_template_class(Kustomization, package=other_templates)
        self.register_patch_class(AddEgressLabelsPatch)
        self.register_patch_file("AntiAffinityPatch")
        self.register_patch_file("HttpProbesPatch")
        self.register_patch_file("MountVolumeFiles")
        self.register_patch_file("KubernetesAnnotations")

    def register_patch_class(self: str, cls: str, aliases=None) -> None:
        super().register_template_class(
            cls,
            filename=None,
            aliases=aliases,
            package=patch_templates)

    def register_patch_file(self,
                            kind: str = None,
                            aliases=None) -> None:
        super().register_template_file(
            kind=kind,
            cls=Patch,
            aliases=aliases,
            package=patch_templates)

    def kreate_komponents_from_strukture(self):
        super().kreate_komponents_from_strukture()
        for res in self.komponents:
            if isinstance(res, Resource):
                self.kreate_patches(res)

    def kreate_patch(
            self,
            res: Resource,
            kind: str = None,
            shortname: str = None,
            **kwargs):
        cls = self.kind_classes[kind]
        templ = self.kind_templates[kind]
        if issubclass(cls, Patch):
            return cls(res, shortname, kind, template=templ, **kwargs)
        raise TypeError(
            f"class for {kind}.{shortname} is not a Patch but {cls}")

    def kreate_patches(self, res: Resource) -> None:
        if "patches" in res.strukture:
            for kind in sorted(res.strukture.patches.keys()):
                subpatches = res.strukture.patches[kind]
                if not subpatches.keys():
                    subpatches = {"main": {}}
                # use sorted because some patches, e.g. the MountVolumes
                # result in a list, were the order can be unpredictable
                for shortname in sorted(subpatches.keys()):
                    self.kreate_patch(res, kind=kind, shortname=shortname)


class Kustomization(JinYamlKomponent):
    def resources(self):
        return [
            res for res in self.app.komponents if isinstance(
                res, Resource)]

    def patches(self):
        return [res for res in self.app.komponents if isinstance(res, Patch)]

    @property
    def filename(self):
        return "kustomization.yaml"
