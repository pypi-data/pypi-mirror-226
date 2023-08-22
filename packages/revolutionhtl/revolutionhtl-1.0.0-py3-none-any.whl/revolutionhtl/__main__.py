if __name__ == "__main__":
    from .reconciliation import reconciliate_many, recon_table_to_str
    from .error import InconsistentTrees, MissedData, ParameterError
    from .orthology import orthologs_from_trees_df
    from .supertree import from_gene_forest
    from .constants import _df_matches_cols, _default_f
    from .hug_free import build_graph_series
    from .parse_prt import _parse, normalization_modes, normalization_smallest
    from .common_tools import norm_path
    from .cBMG_tools import analyze_digraphs_list
    from .nhxx_tools import read_nhxx, get_nhx
    from .in_out import read_tl_digraph, tl_digraph_from_pandas

    from tqdm import tqdm
    from numpy import argsort
    import pandas as pd
    import os

    import argparse
    parser = argparse.ArgumentParser(prog= 'revolutionhtl',
                                     description='Bioinformatics tool for the reconstruction of evolutionaty histories. https://gitlab.com/jarr.tecn/revolutionh-tl/',
                                    )

    # Parameters
    ############

    parser.add_argument('-steps',
                        help= 'List of steps to run (default: 1 2 3 4).',
                        type= int,
                        nargs= '*',
                        default= [1, 2, 3, 4]
                       )

    parser.add_argument('-blast_h', '--blast_hits',
                        help= 'Directory containing pairwise blast-like analysis (default: ./).',
                        type= str,
                       )

    parser.add_argument('-best_h', '--best_hits',
                        help= '.tsv file containing best hits (putative best matches).',
                        type= str,
                       )

    parser.add_argument('-T', '--gene_trees',
                        help= '.tsv file containing a .nhx for each line at column "tree"',
                        type= str,
                       )

    parser.add_argument('-S', '--species_tree',
                        help= '.nhx file containing a species tree, or the key word BUILD_FROM_GENE_FOREST to infer an species tree as the maximum set of species triples [REFERENCE].',
                        type= str,
                        default= 'BUILD_FROM_GENE_FOREST',
                       )

    parser.add_argument('-f', '--f_value',
                        help= f'Real number between 0 and 1 used for the adaptative threshhold for best matches selection: f*max_bit_score (default {_default_f}).',
                        type= float,
                        default= _default_f,
                       )

    parser.add_argument('-pm', '--partition_method',
                        help= f'Partition method for bmg editing. Most precise: Louvain.',
                        type= str,
                        default= 'Louvain',
                        choices= ['Mincut', 'BPMF', 'Karger', 'Greedy', 'Gradient_Walk', 'Louvain', 'Louvain_Obj'],
                       )

    parser.add_argument('-C', '--clustering_for_supertree_heuristic',
                        help= 'Meta parameter of the heuristics, specifies a comunity-detection algorithm. See more in [REFERENCE]run the algorithm for community detection',
                        type= str,
                        default= 'louvain_weight',
                        choices= ['naive', 'louvain', 'mincut', 'louvain_weight']
                       )

    parser.add_argument('-Cr', '--repeats_for_clustering',
                        help= 'Meta parameter of the heuristics, specifies how many time run the algorithm for community detection',
                        type= int,
                        default= 3
                       )

    parser.add_argument('-build2', '--doble_build',
                        help= 'Run build algorithm twice aimed to obtain less-resolved tree. See [REFERENCE]',
                        type= bool,
                        default= True,
                       )

    parser.add_argument('-o', '--output_prefix',
                        help= 'Prefix used for output files (default "tl_project").',
                        type= str,
                        default= 'tl_project',
                       )

    parser.add_argument('-rod', '--recon_output_dir',
                        help= 'Directory for reconciliation maps (default: ./).',
                        type= str,
                        default= './',
                       )

    parser.add_argument('-og', '--orthogroup_column',
                        help= 'Column in -best_hits and -gene_trees specifying orthogroups (default: OG).',
                        type= str,
                        default= 'OG',
                       )

    parser.add_argument('-bhsm', '--bhs_mode',
                        help= 'Mode for best hit selection: normal or proteinortho. The former only uses dinamic threshold, the later integrates proteinortho orthogroups (default: normal).',
                        type= str,
                        choices= ['normal', 'prt']+normalization_smallest+normalization_modes,
                        default= 'normal',
                       )

    parser.add_argument('-Nm', '--N_max',
                        help= 'Maximum number of genes in a orthogroup. If 0, all orthogroups will be analized. (default= 2000)',
                        type= int,
                        default= 2000,
                       )

    parser.add_argument('-k', '--k_size_partition',
                        help= 'Partition of best hit graphs w.r.t. number of genes: first will be procesesd graphs with <k genes, then <2k. then <3k, and so on. (default: k=100)',
                        type= int,
                        default= 100,
                       )



    args= parser.parse_args()
    args.recon_output_dir= norm_path(args.recon_output_dir)

    ################
    # Process data #
    ################

    from .hello import hello5
    print(hello5)

    allowed_steps= {1, 2, 3, 4}
    bad_steps= set(args.steps) - allowed_steps
    if len(bad_steps) > 0:
        raise ParameterError(f'Only steps 1, 2, and 3 are allowed to be used in the parameter -steps. ')
    else:
        args.steps= sorted(set(args.steps))

    print(f'Running steps {", ".join(map(str, args.steps))}')

    # 1. Convert proteinortho output to a best-hit list
    #################################################
    if 1 in args.steps:
        print("\nStep 1: Convert proteinortho output to a best-hit list")
        print("------------------------------------------------------")
        if args.blast_hits==None:
            raise MissedData('Step 0 needs a value for the parameter -blast_hits.')

        args.blast_hits= norm_path(args.blast_hits)
        opath= args.output_prefix+'.best_hits.tsv'
        df_hits, OGs_table= _parse(args.blast_hits, args.f_value, opath, args.bhs_mode, N_max= args.N_max)
        print('This file will be used as input for step 2.')

        print('Writing orthogroups...')
        opath= args.output_prefix+'.orthogroups.tsv'
        OGs_table.to_csv(opath, sep='\t', index= False)
        print(f'Successfully written to {opath}')
    else:
        df_hits= None

    # 2. Conver best hit graphs to cBMGs and gene trees
    ##################################################
    if 2 in args.steps:
        print("\nStep 2: Conver best-hit graphs to cBMGs and gene trees")
        print("------------------------------------------------------")
        readHs= type(df_hits)!=pd.DataFrame
        if readHs and (args.best_hits==None):
            raise MissedData('Step 2 needs a value for the parameter -best_hits. Create it by running step 1.')

        if readHs:
            print('Reading hit graphs...')
            G= read_tl_digraph(args.best_hits, og_col= args.orthogroup_column)
        else:
            print('Creating graphs...')
            G= tl_digraph_from_pandas(df_hits, og_col= args.orthogroup_column)

        Tg= build_graph_series(G, args)

        # Print orthologs
        TTg= Tg.reset_index()
        df_orthologs= orthologs_from_trees_df(TTg,
                                forbidden_leaf_name= 'X', tree_col= 'tree')
        opath= f'{args.output_prefix}.orthologs.tsv'
        df_orthologs.to_csv(opath, sep= '\t', index= False)
        print(f'Orthologs successfully written to {opath}')


    else:
        Tg= None

    # 3. Reconstruct species tree
    #############################
    if 3 in args.steps:
        print("\nStep 3: Species tree reconstruction")
        print("-----------------------------------")
        readTg= type(Tg)!=pd.Series
        if readTg and (args.gene_trees==None):
            raise MissedData('Step 3 needs a value for the parameter -gene_trees. Create it by running step 2.')
        if readTg:
            print('Reading trees...')
            gTrees= pd.read_csv(args.gene_trees,
                                sep= '\t').set_index(
                args.orthogroup_column).tree.apply(lambda x: read_nhxx(x, name_attr= 'accession'))
        else:
            gTrees= Tg

        print("Reconstructing species tree...")
        species_tree= from_gene_forest(gTrees,
                                       method= args.clustering_for_supertree_heuristic,
                                       numb_repeats= args.repeats_for_clustering,
                                       doble_build= args.doble_build
                                      )

        print("Writing species tree...")
        s_newick= get_nhx(species_tree, root= 1, name_attr= 'species', ignore_inner_name= True)
        opath= f'{args.output_prefix}.species_tree.tsv'
        with open(opath, 'w') as F:
            F.write(s_newick)
        print(f'Successfully written to {opath}')
    else:
        species_tree= None

    # 4. Reconciliate gene trees and species tree
    ##############################################
    if 4 in args.steps:
        print("\nStep 4: Reconciliation of gene species trees")
        print("--------------------------------------------")
        readTg= type(Tg)!=pd.Series
        if readTg:
            if args.gene_trees==None:
                raise MissedData('Step 4 needs a value for the parameter -gene_trees. You can create it by running step 2.')
            print('Reading trees...')
            gTrees= pd.read_csv(args.gene_trees,
                                sep= '\t').set_index(
                args.orthogroup_column).tree.apply(lambda x: read_nhxx(x, name_attr= 'accession'))
        else:
            gTrees= Tg

        readTs= species_tree == None
        if readTs:
            if args.species_tree=='BUILD_FROM_GENE_FOREST':
                raise MissedData('Step 4 needs a species tree, run step 3 to construct one or set a value for the parameter -species_tree')
            if not os.path.isdir(args.recon_output_dir):
                raise ValueError(f'-recon_output_dir {args.recon_output_dir}: : No such directory')
            print('Reading species tree...')
            with open(args.species_tree) as F:
                sTree= read_nhxx(''.join( F.read().strip().split('\n') ),
                                 name_attr= 'species')
        else: 
            sTree= species_tree

        print('Reconciling trees...')
        df_recs= reconciliate_many(gTrees, sTree)

        # Write resolved trees
        df_r= recon_table_to_str(sTree, df_recs, args.orthogroup_column)
        print("Writing to file...")
        opath= f'{args.output_prefix}.reconciliation.tsv'
        df_r.to_csv(opath, sep= '\t', index= False)
        print(f'Reconciliation were successfully written to {opath}')

        # Write labeled species tree
        nhx_s= get_nhx(sTree, name_attr= 'species', root= 1, ignore_inner_name= True)
        opath= f'{args.output_prefix}.labeled_species_tree.nhxx'
        with open(opath, 'w') as F:
            F.write(nhx_s)
        print(f'Indexed species tree successfully written to {opath}')

        """
        # Write orthology relations
        df_orthologs, df_pseudo= orthologs_from_trees_df(df_recs, forbidden_leaf_name= 'X', tree_col= 'reconciliated_tree')

        opath= f'{args.output_prefix}.orthologs.tsv'
        df_orthologs.to_csv(opath, sep= '\t', index= False)
        print(f'Orthologs successfully written to {opath}')

        opath= f'{args.output_prefix}.pseudo_orthologs.tsv'
        df_pseudo.to_csv(opath, sep= '\t', index= False)
        print(f'Pseudo-orthologs successfully written to {opath}')
        """

    print("\nREvolutionH-tl finished all the tasks without any problem")
    print("---------------------------------------------------------")
