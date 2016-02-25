from multiprocessing.pool import ThreadPool


def get_link_names_from_workerlistgen(container_links):
    names = [link["name"] for link in container_links]
    return names

def get_config_lines(link_names):
    config_lines = [(name + " 5432") for name in link_names]
    return config_lines
