import logging

from grammar_graph.gg import GrammarGraph

from input_constraints.evaluator import grammar_coverage_generator, evaluate_generators
from input_constraints.solver import ISLaSolver, CostSettings, CostWeightVector
from input_constraints.tests.subject_languages import scriptsizec

timeout = 5

cost_vector = CostWeightVector(
    tree_closing_cost=10,
    vacuous_penalty=9,
    constraint_cost=0,
    derivation_depth_penalty=9,
    low_k_coverage_penalty=28,
    low_global_k_path_coverage_penalty=4)

k = 4

g_defuse = ISLaSolver(
    scriptsizec.SCRIPTSIZE_C_GRAMMAR,
    scriptsizec.SCRIPTSIZE_C_DEF_USE_CONSTR,
    max_number_free_instantiations=1,
    max_number_smt_instantiations=1,
    timeout_seconds=timeout,
    cost_settings=CostSettings((cost_vector,), (1000,), k=k)
)

g_redef = ISLaSolver(
    scriptsizec.SCRIPTSIZE_C_GRAMMAR,
    scriptsizec.SCRIPTSIZE_C_NO_REDEF_CONSTR,
    max_number_free_instantiations=1,
    max_number_smt_instantiations=1,
    timeout_seconds=timeout,
    cost_settings=CostSettings((cost_vector,), (1000,), k=k)
)

g_defuse_redef = ISLaSolver(
    scriptsizec.SCRIPTSIZE_C_GRAMMAR,
    scriptsizec.SCRIPTSIZE_C_DEF_USE_CONSTR & scriptsizec.SCRIPTSIZE_C_NO_REDEF_CONSTR,
    max_number_free_instantiations=1,
    max_number_smt_instantiations=1,
    timeout_seconds=timeout,
    cost_settings=CostSettings((cost_vector,), (1000,), k=k)
)


def evaluate_validity():
    logging.basicConfig(level=logging.DEBUG)

    out_dir = "../../eval_results/xml"
    base_name = "input_validity_xml_"

    generators = [scriptsizec.SCRIPTSIZE_C_GRAMMAR, g_defuse, g_redef, g_defuse_redef]
    results = evaluate_generators(
        generators,
        None,
        GrammarGraph.from_grammar(scriptsizec.SCRIPTSIZE_C_GRAMMAR),
        scriptsizec.compile_scriptsizec_clang,
        timeout,
        k=3,
        # cpu_count=len(generators)
        cpu_count=1
    )

    results[0].save_to_csv_file(out_dir, base_name + "g_rand")
    results[1].save_to_csv_file(out_dir, base_name + "g_defuse")
    results[2].save_to_csv_file(out_dir, base_name + "g_redef")
    results[3].save_to_csv_file(out_dir, base_name + "g_defuse_redef")


if __name__ == '__main__':
    evaluate_validity()
