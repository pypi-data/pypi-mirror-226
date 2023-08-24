import pytest

# attempt to replicate grid boundary probability and entropy (H) from 
# Brewer, Juybari, Moberly (2023), J. Econ Interact Coord, Tab.5
# https://link.springer.com/article/10.1007/s11403-023-00387-8/tables/5
# grid size 20 only active for testing
# grid size 40 is commented out because of low RAM on github actions but can be tested manually by removing '#'

@pytest.mark.parametrize("params,correct", [
    ({'g':20,'zi':False}, {'p_boundary': 0.024, 'p_voter_ideal_point_triangle': 0.458, 'entropy': 10.32}),
    ({'g':20,'zi':True},  {'p_boundary': 0.0086,'p_voter_ideal_point_triangle': 0.68, 'entropy':  9.68}),
#   ({'g':40,'zi':False}, {'p_boundary': 0.000254, 'p_voter_ideal_point_triangle':0.396, 'entropy': 10.92}),
#   ({'g':40,'zi':True},  {'p_boundary': 2.55e-05, 'p_voter_ideal_point_triangle':0.675, 'entropy': 9.82})
])
def test_replicate_spatial_voting_analysis(params, correct):
    import gridvoting as gv
    np = gv.np
    xp = gv.xp
    g = params['g']
    zi = params['zi']
    majority = 2
    grid = gv.Grid(x0=-g,x1=g,y0=-g,y1=g)
    number_of_alternatives = (2*g+1)*(2*g+1)
    assert len(grid.x) == number_of_alternatives
    assert len(grid.y) == number_of_alternatives
    voter_ideal_points = np.array([
        [-15,-9],
        [0,17],
        [15,-9]
    ])
    number_of_voters = 3
    assert voter_ideal_points.shape == (3,2)
    u = grid.spatial_utilities(
        voter_ideal_points=voter_ideal_points,
        metric='sqeuclidean'
    )
    assert u.shape == (number_of_voters, number_of_alternatives)
    vm = gv.VotingModel(
        utility_functions=u,
        majority=majority,
        zi=zi,
        number_of_voters=number_of_voters,
        number_of_feasible_alternatives=number_of_alternatives
    )
    vm.analyze()
    stat_dist = vm.stationary_distribution
    assert stat_dist.sum() == pytest.approx(1.0,abs=1e-9)
    p_boundary = stat_dist[grid.boundary].sum()
    assert p_boundary == pytest.approx(correct['p_boundary'], rel=0.05)
    triangle_of_voter_ideal_points = grid.within_triangle(points=voter_ideal_points)
    p_voter_ideal_point_triangle = stat_dist[triangle_of_voter_ideal_points].sum()
    assert p_voter_ideal_point_triangle == pytest.approx(correct['p_voter_ideal_point_triangle'], rel=0.05)
    stat_dist_gz = stat_dist[stat_dist>0.0]
    entropy = -stat_dist_gz.dot(np.log2(stat_dist_gz))
    assert entropy == pytest.approx(correct['entropy'], abs=0.01)
    stat_dist_algebraic = xp.asnumpy(vm.MarkovChain.solve_for_unit_eigenvector())
    l1_power_vs_algebraic_solns = np.linalg.norm(stat_dist-stat_dist_algebraic, ord=1)
    assert l1_power_vs_algebraic_solns < 1e-9
