def pos_tagging(R, S, T, E):
    tags = dict()
    for s in S:
        tags[s] = R[0]
    return tags
