from ir.nodes import *
from frame.frame import Frame


class Block:
    """Block commencant par un label et terminant par un (c)jump"""

    def __init__(self, name, stms, start, end=False, cjump=None, jump=None, jumpTrue=None, jumpFalse=None):
        assert isinstance(name, Label), "name must be a Label"
        assert isinstance(stms, list), "stms must be a list of Stm"
        assert jump is None or isinstance(jump, Label), "jump must be a Label"
        assert jumpTrue is None or isinstance(jumpTrue, Label), "jumpTrue must be a Label"
        assert jumpFalse is None or isinstance(jumpFalse, Label), "jumpFalse must be a Label"
        self.name      = name
        self.stms      = stms
        self.cjump     = cjump
        self.jump      = jump
        self.jumpTrue  = jumpTrue
        self.jumpFalse = jumpFalse
        self.start     = start
        self.end       = end
        self.exam      = end

def reorder_blocks(seq, frame):
    """Reorder blocks in seq so that the negative branch of a CJUMP always
    follows the CJUMP itself. frame is the frame of the corresponding
    function."""
    assert(isinstance(seq, SEQ))
    assert(isinstance(frame, Frame))

    # Ajout des jumps a la fin de chaque block n'en possedant pas
    # Rempli le dictionnaire contenant les blocks commancant par un label
    # et finnissant par un (c)jump
    dico = init_dico(seq)

    # Réordonne les blocks du dico
    list_reorder = init_list(dico)

    # Suppression des jump inutile
    list_reorder = linearisation(list_reorder)

    # Cette concaténation deviens le nouveau corps du nœud SEQ
    seq.stms = list_reorder
    return seq


def init_dico(seq):

    is_block = False
    first_block = True
    dico = {}
    list = []
    name = ""

    for stm in seq.stms:
        if isinstance(stm, LABEL):
            # Ajout d'un jump
            if is_block:
                list.append(JUMP(NAME(stm.label)))
                dico[name] = Block(name=name, stms=list, start=first_block, \
                                   cjump=False, jump=stm.label)
                if first_block: first_block = False
            # Initialisation name, list et is_block
            name = stm.label
            list = [stm]
            is_block = True
        elif isinstance(stm, JUMP):
            list.append(stm)
            dico[name] = Block(name=name, stms=list, start=first_block, \
                               cjump=False, jump=stm.target.label)
            if first_block: first_block = False
            is_block = False
        elif isinstance(stm, CJUMP):
            list.append(stm)
            dico[name] = Block(name=name, stms=list, start=first_block, \
                               cjump=True, jumpTrue=stm.ifTrue.label, \
                               jumpFalse=stm.ifFalse.label)
            if first_block: first_block = False
            is_block = False
        else:
            list.append(stm)
    # ajout du label end sans jump
    dico[name] = Block(name=name, stms=list, start=False, end=True)
    return dico


def init_list(dico):

    list = []

    # ajout du start au début de la liste
    for block in dico.values():
        if block.start:
            for stm in analyse(block, dico):
                list.append(stm)

    # ajout des blocks autres dans la liste
    for block in dico.values():
        for stm in analyse(block, dico):
            list.append(stm)

    # ajout du end à la fin de la liste
    for block in dico.values():
        if block.end:
            for stm in block.stms:
                list.append(stm)
    return list


def analyse(block, dico):

    list = []
    next_label = ""

    if not block.exam:
        block.exam = True
        if block.cjump:
            # saut conditionnel
            next_label = block.jumpFalse
            if dico[next_label].exam:
                next_label = block.jumpTrue
                if dico[next_label].exam:
                    # jump vers un label fictif
                    label = block.jumpFalse.name
                    next_label = label + "Fictif"

                    # ajout d'un block fictif contenant un label et un jump
                    # dans le block courant
                    block.stms.append(Label(next_label))
                    block.stms.append(JUMP(NAME(Label(label))))

                    # MaJ de la destination en cas d'une condition fausse
                    block.stms[-1].ifFalse = NAME(Label(next_label))
                    block.jumpFalse = NAME(Label(next_label))
                else:
                    # inversion de la condition et des labels vrai faux
                    block.stms[-1].op = oppo(block.stms[-1].op)
                    block.stms[-1].ifTrue, block.stms[-1].ifFalse = \
                        block.stms[-1].ifFalse, block.stms[-1].ifTrue
        else:
            # saut inconditionnel
            next_label = block.jump

        # ajout du block courant à la liste
        for stm in block.stms:
            list.append(stm)

        # on continue vers le block pointé par le jump
        if next_label in dico:
            for stm in analyse(dico[next_label], dico):
                list.append(stm)
    return list

def oppo(str):
    if   str == "<":  return ">="
    elif str == "<=": return ">"
    elif str == ">":  return "<="
    elif str == ">=": return "<"
    elif str == "=":  return "<>"
    elif str == "<>": return "="
    else: raise AssertionError("Opperande doesn't manage %s" % str)

def linearisation(list):
    i = 0
    for l in list:
        if isinstance(l, LABEL):
            if isinstance(list[i-1], JUMP) and list[i-1].target.label == l.label:
                list.pop(i-1)
        i = i+1
    return list
