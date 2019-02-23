from FormRadixTree import FormRadixTree

if __name__ == "__main__":
    # f = FormRadixTree().get()
    rtree = FormRadixTree().get()

    print("Test print nodes")
    print('Prefix\tvisibility\tlast_seen')
    for node in rtree:
        print(node.prefix + '\t' + str(node.data['visibility']) + '\t' + str(node.data['last_seen']))