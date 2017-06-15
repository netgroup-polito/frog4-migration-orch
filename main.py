from config import Configuration
from controllers.main_controller import MainController
from utils import dump_json_file
import logging

if __name__ == "__main__":

    logging.info("frog4-migration-orch started...")

    mainController = MainController()
    graphs_path = Configuration().GRAPHS_PATH
    graph_id = None

    print("1] Deploy a graph")
    print("2] Migrate graph to another domain")
    print("3] Migrate status")
    print("4] Delete old graph")
    print("0] Reset")
    print("9] Exit")

    while True:

        cmd = input("Choose action: ")

        if cmd == "1":
            nffg_json = dump_json_file(graphs_path+"/graph1.json")
            graph_id = mainController.deploy_graph(nffg_json)

        if cmd == "2":
            nffg_json = dump_json_file(graphs_path + "/graph1.json")
            mainController.migrate_nf(graph_id, nffg_json)

        if cmd == "3":
            mainController.migrate_status()

        if cmd == "4":
            nffg_json = dump_json_file(graphs_path + "/graph1.json")
            mainController.delete_old_nf(graph_id, nffg_json)

        if cmd == "0":
            mainController.reset()

        if cmd == "9":
            break

        else:
            print("Error, invalid command")

    logging.info("frog4-migration-orch stopped!")


