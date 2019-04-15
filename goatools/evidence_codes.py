"""Manage evidence codes as reported by the Gene Ontology Consortium."""

__copyright__ = "Copyright (C) 2016-2019, DV Klopfenstein, H Tang. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import collections as cx


# pylint: disable=line-too-long
class EvidenceCodes(object):
    """From http://geneontology.org/page/guide-go-evidence-codes"""
    # gocwiki.geneontology.org/index.php/Evidence_Code_Ontology_%28ECO%29

    ntobj = cx.namedtuple("NtCode", "eco group name")

    code2name = cx.OrderedDict([
        # Experimental Evidence codes:
        ("EXP", ntobj._make(["ECO:0000269", "Experimental", "Inferred from Experiment"])),
        ("IDA", ntobj._make(["ECO:0000314", "Experimental", "Inferred from Direct Assay"])),
        ("IPI", ntobj._make(["ECO:0000353", "Experimental", "Inferred from Physical Interaction"])),
        ("IMP", ntobj._make(["ECO:0000315", "Experimental", "Inferred from Mutant Phenotype"])),
        ("IGI", ntobj._make(["ECO:0000316", "Experimental", "Inferred from Genetic Interaction"])),
        ("IEP", ntobj._make(["ECO:0000270", "Experimental", "Inferred from Expression Pattern"])),

        # Similarity evidence codes
        ("ISS", ntobj._make(["ECO:0000250", "Similarity", "Inferred from Sequence or structural Similarity"])),
        ("ISO", ntobj._make(["ECO:0000266", "Similarity", "Inferred from Sequence Orthology"])),
        ("ISA", ntobj._make(["ECO:0000247", "Similarity", "Inferred from Sequence Alignment"])),
        ("ISM", ntobj._make(["ECO:0000255", "Similarity", "Inferred from Sequence Model used in manual assertion"])),
        ("IGC", ntobj._make(["ECO:0000317", "Similarity", "Inferred from Genomic Context"])),
        ("IBA", ntobj._make(["ECO:0000318", "Similarity", "Inferred from Biological aspect of Ancestor"])),
        ("IBD", ntobj._make(["ECO:0000319", "Similarity", "Inferred from Biological aspect of Descendant"])),
        ("IKR", ntobj._make(["ECO:0000320", "Similarity", "Inferred from phylogenetic determination of loss of key residues (manual assertion)"])),
        ("IRD", ntobj._make(["ECO:0000321", "Similarity", "Inferred from Rapid Divergence from ancestral sequence (manual assertion)"])),
        ("IMR", ntobj._make(["ECO:0000320", "Similarity", "Phylogenetic determination of loss of key residues in manual assertion"])),

        # Combinatorial evidence codes
        ("RCA", ntobj._make(["ECO:0000245", "Combinatorial", "Inferred from Reviewed Computational Analysis"])),

        # High Throughput Experimental evidence codes
        ("HTP", ntobj._make(["ECO:0006056", "High_Throughput", "Inferred from High Throughput Experimental"])),
        ("HDA", ntobj._make(["ECO:0007005", "High_Throughput", "Inferred from High Throughput Direct Assay"])),
        ("HMP", ntobj._make(["ECO:0007001", "High_Throughput", "Inferred from High Throughput Mutant Phenotype"])),
        ("HGI", ntobj._make(["ECO:0007003", "High_Throughput", "Inferred from High Throughput Genetic Interaction"])),
        ("HEP", ntobj._make(["ECO:0007007", "High_Throughput", "Inferred from High Throughput Expression Pattern"])),

        # Author Statement evidence codes
        ("TAS", ntobj._make(["ECO:0000304", "Author", "Traceable Author Statement used in manual assertion"])),
        ("NAS", ntobj._make(["ECO:0000303", "Author", "Non-traceable Author Statement used in manual assertion"])),

        # Curator Inference
        ("IC", ntobj._make(["ECO:0000305", "Curatorial", "Inferred by Curator"])),

        # No Biological Data
        ("ND", ntobj._make(["ECO:0000307", "No biological data", "No biological Data available"])),

        # Automatic Assertion
        ("IEA", ntobj._make(["ECO:0000501", "Automatic", "Inferred from Electronic Annotation"]))])

    ev2idx = {ev:i for i, ev in enumerate(code2name.keys())}

    def sort_nts(self, nt_list, codekey):
        """Sort list of namedtuples such so evidence codes in same order as code2name."""
        # Problem is that some members in the nt_list do NOT have
        # codekey=EvidenceCode, then it returns None, which breaks py34 and 35
        # The fix here is that for these members, default to -1 (is this valid?)
        sortby = lambda nt: self.ev2idx.get(getattr(nt, codekey), -1)
        return sorted(nt_list, key=sortby)

    def get_grp_name(self, code):
        """Return group and name for an evidence code."""
        nt_code = self.code2name.get(code, None)
        if nt_code is not None:
            return nt_code.group, nt_code.name
        return "", ""

    def prt_ev_cnts(self, ctr, prt=sys.stdout):
        """Prints evidence code counts stored in a collections Counter."""
        for key, cnt in ctr.most_common():
            grp, name = self.get_grp_name(key.replace("NOT ", ""))
            prt.write("{CNT:7,} {EV:>7} {GROUP:<15} {NAME}\n".format(
                CNT=cnt, EV=key, GROUP=grp, NAME=name))

    def get_order(self, codes):
        """Return evidence codes in order shown in cod2name."""
        return sorted(codes, key=lambda e: [self.ev2idx.get(e)])

    def prt_summary_anno2ev(self, associations, prt=sys.stdout):
        """Print annotation/evidence code summary."""
        ctr = cx.Counter()
        for ntanno in associations:
            evidence_code = ntanno.Evidence_Code
            if 'NOT' not in ntanno.Qualifier:
                ctr[evidence_code] += 1
            elif 'NOT' in ntanno.Qualifier:
                ctr["NOT {EV:3}".format(EV=ntanno.Evidence_Code)] += 1
            else:
                raise Exception("UNEXPECTED INFO")
        self.prt_ev_cnts(ctr, prt)

# Copyright (C) 2016-2019, DV Klopfenstein, H Tang. All rights reserved."
