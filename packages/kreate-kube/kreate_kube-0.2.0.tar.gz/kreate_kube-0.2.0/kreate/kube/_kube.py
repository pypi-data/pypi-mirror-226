import os
import shutil
import logging
from ..kore import JinjaApp, Konfig
from ..krypt import KryptKonfig, krypt_functions
from ..kore import _jinyaml
from . import resource, other_templates, resource_templates

logger = logging.getLogger(__name__)


class KubeApp(JinjaApp):
    def __init__(self, konfig: Konfig):
        super().__init__(konfig)
        self.namespace = self.appname + "-" + self.env

    def register_std_templates(self) -> None:
        super().register_std_templates()
        self.register_resource_class(resource.Service, "svc")
        self.register_resource_class(resource.Deployment, "depl")
        self.register_resource_class(resource.PodDisruptionBudget, "pdb")
        self.register_resource_class(resource.ConfigMap, "cm")
        self.register_resource_class(resource.Ingress)
        self.register_resource_class(resource.Egress)
        self.register_resource_class(resource.SecretBasicAuth)
        self.register_resource_class(resource.Secret)

        self.register_resource_file("HorizontalPodAutoscaler", aliases="hpa")
        self.register_resource_file("ServiceAccount")
        self.register_resource_file("ServiceMonitor")
        self.register_resource_file("CronJob")
        self.register_resource_file("StatefulSet", filename="Deployment.yaml")

    def register_resource_class(self: str, cls: str, aliases=None) -> None:
        super().register_template_class(
            cls,
            filename=None,
            aliases=aliases,
            package=resource_templates)

    def register_resource_file(self,
                               cls: str,
                               filename: str = None,
                               aliases=None) -> None:
        super().register_template_file(
            cls,
            filename=filename,
            aliases=aliases,
            package=resource_templates)

    def _default_template_class(self):
        return resource.Resource

    def aktivate(self):
        target_dir = self.konfig.target_dir
        if os.path.exists(target_dir) and os.path.isdir(target_dir):
            logger.info(f"removing target directory {target_dir}")
            shutil.rmtree(target_dir)
        self.konfig.kopy_files("files", "files")
        self.konfig.kopy_files("secret_files", "secrets/files", dekrypt_default=True)
        super().aktivate()


class KubeKonfig(KryptKonfig):
    def kopy_files(self, key, target_subdir, dekrypt_default=False):
        file_list = self.yaml.get(key, [])
        if not file_list:
            return
        os.makedirs(f"{self.target_dir}/{target_subdir}", exist_ok=True)
        for file in file_list:
            dekrypt = file.get("dekrypt", dekrypt_default)
            name = file.get("name", None)
            if not name:
                raise ValueError(f"file in konfig {key}"
                                 f"should have name {file}")
            from_ = file.get("from", f"{key}/{name}"
                             + (".encrypted" if dekrypt else ""))
            template = file.get("template", False)
            loc = _jinyaml.FileLocation(from_, dir=self.dir)
            if template:
                vars = {
                        "konfig": self,
                        "val": self.values,
                        "secret": self.secrets,
                }
                logger.debug(f"rendering template {from_}")
                prefix = "rendered template " + from_
                data = _jinyaml.load_jinja_data(loc, vars)
            else:
                prefix = from_
                data = _jinyaml.load_data(loc)
            if dekrypt:
                prefix = "dekrypted "+ prefix
                data = krypt_functions.dekrypt_str(data)
            with open(f"{self.target_dir}/{target_subdir}/{name}", "w") as f:
                logger.info(f"kreating file {key}/{name} from {prefix}")
                f.write(data)


# Note the KubeKonfig class is totally unrelated to the
# kubeconfig file
def kreate_kubeconfig(konfig: Konfig):
    cluster_name = konfig.values.get("kubeconfig_cluster_name", None)
    if not cluster_name:
        cluster_name = f"{konfig.env}-cluster"
    user_name = konfig.values.get("kubeconfig_cluster_user_name", None)
    if not user_name:
        user_name = f"kreate-user-{konfig.env}"
    context_name = konfig.env
    # api_token should not be set in a file, just as environment variable
    token = os.getenv("KUBECONFIG_API_TOKEN")
    if not token:
        raise ValueError("environment var KUBECONFIG_API_TOKEN not set")
    api_token = token
    my = {
        "cluster_name": cluster_name,
        "cluster_user_name": user_name,
        "context_name": context_name,
        "api_token": api_token,
    }
    vars = {
            "konfig": konfig,
            "my": my,
            "val": konfig.values
        }
    loc = _jinyaml.FileLocation("kubeconfig.yaml", package=other_templates)
    data = _jinyaml.load_jinja_data(loc, vars)
    filename = f"{konfig.target_dir}/secrets/kubeconfig"
    logging.info(f"writing {filename}")
    os.makedirs(f"{konfig.target_dir}/secrets", exist_ok=True)
    with open(filename, "wt") as f:
        f.write(data)
