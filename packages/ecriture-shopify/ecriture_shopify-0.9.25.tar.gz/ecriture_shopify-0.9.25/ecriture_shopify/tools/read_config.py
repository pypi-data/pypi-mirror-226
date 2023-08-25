# library
import json
import tomllib


#
def get_pypt_version(path_pypt):
    """fonction pour récupérer la version du pyproject.toml, définie ici et uniquement ici"""
    with open(path_pypt, "rb") as f:
        return tomllib.load(f)["tool"]["poetry"]["version"]


#
def get_config_jsonc(path_json):
    """pour charger un json et supprimer les commentaires s'il y en a."""
    with open(path_json, "r", encoding="utf-8") as f:
        # json as list of str
        full_json_list = f.readlines()
        # remove the comments: '//' in json
        clean_json_list = [line for line in full_json_list if not line.strip().startswith("//")]
        # join to make it 'json.loads' read
        clean_json_str = "\n".join(clean_json_list)

        return json.loads(clean_json_str)


# end
