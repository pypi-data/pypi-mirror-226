import numpy as np
import GCRCatalogs
from GCRCatalogs.helpers.tract_catalogs import tract_filter, sample_filter
from astropy.table import Table
from astropy.io import fits

#######################################################
#Copied from cluster_validation package (from M. Ricci)
#######################################################

def RM_DC2_cat_open(RM_cat_name, DC2_cat_name, min_richness=20, min_halo_mass=1e14, cluster_only=True):
	# Get the redMaPPer catalog
	gc = GCRCatalogs.load_catalog(RM_cat_name)
	# Select out the cluster and member quantities into different lists
	quantities = gc.list_all_quantities()
	cluster_quantities = [q for q in quantities if 'member' not in q]
	member_quantities = [q for q in quantities if 'member' in q]
	
	# Read in the cluster and member data
	query = GCRCatalogs.GCRQuery('(richness > ' + str(min_richness)+')')
	#query = sample_filter(0.0001)
	
	#cluster_data = Table(gc.get_quantities(cluster_quantities, [query]))
	cluster_data = Table(gc.get_quantities(cluster_quantities))
	member_data = Table(gc.get_quantities(member_quantities))
	
	#read in the "truth" catalog as a comparison (can take a while...)
	gc_truth = GCRCatalogs.load_catalog(DC2_cat_name)  
	quantities_wanted = ['redshift','halo_mass','halo_id','galaxy_id','ra','dec', 'is_central']
	if cluster_only :
	    query = GCRCatalogs.GCRQuery('(is_central == True) & (halo_mass > ' + str(min_halo_mass) +')')
	else :
	    query = GCRCatalogs.GCRQuery('(halo_mass > ' + str(min_halo_mass) +')')
	    
	truth_data = Table(gc_truth.get_quantities(quantities_wanted, [query]))
	
	return cluster_data, member_data, truth_data, gc, gc_truth

def DC2_cat_open(DC2_cat_name, min_halo_mass=1e14, cluster_only=True):
	#read in the "truth" catalog as a comparison (can take a while...)
	gc_truth = GCRCatalogs.load_catalog(DC2_cat_name)  
	quantities_wanted = ['redshift','halo_mass','halo_id','galaxy_id','ra','dec','is_central']#,'baseDC2/sod_halo_mass']
	if cluster_only :
	    query = GCRCatalogs.GCRQuery('(is_central == True) & (halo_mass > ' + str(min_halo_mass) +')')
	    truth_data = Table(gc_truth.get_quantities(quantities_wanted, [query]))
	    exg = Table(fits.open('/sps/lsst/groups/clusters/dc2/cosmoDC2_v1.1.4/extragal/halos/halos_m200c_13.0.fits')[1].data)

	    ## LOOK AT ONLY THOSE HALOS SHARED BETWEEN CATALOGS
	    gcr_in_exg = np.isin(truth_data['halo_id'], exg['halo_id'])
	    exg_in_gcr = np.isin(exg['halo_id'], truth_data['halo_id'])
	    truth_data = truth_data[gcr_in_exg]
	    exg = exg[exg_in_gcr]

	    truth_data.sort('halo_id')
	    exg.sort('halo_id')

	    truth_data['m200c'] = exg['m200c']
	else :
	    query = GCRCatalogs.GCRQuery('(halo_mass > ' + str(min_halo_mass) +')')
	    truth_data = Table(gc_truth.get_quantities(quantities_wanted, [query]))
	    exg = Table(fits.open('/sps/lsst/groups/clusters/dc2/cosmoDC2_v1.1.4/extragal/halos/halos_m200c_13.0.fits')[1].data)
	    
	    ## LOOK AT ONLY THOSE HALOS SHARED BETWEEN CATALOGS
	    gcr_in_exg = np.isin(truth_data['halo_id'], exg['halo_id'])
	    exg_in_gcr = np.isin(exg['halo_id'], truth_data['halo_id'])
	    truth_data = truth_data[gcr_in_exg]
	    exg = exg[exg_in_gcr]

	    truth_data.sort('halo_id')
	    exg.sort('halo_id')

	    ## m200c IS GIVEN ONLY FOR EACH HALO
	    ## BUT WE WANT IT FOR EACH MEMBER
	    ## SO WE HAVE TO MATCH THE HALOS IN ONE CATALOG TO THE MEMBERS IN THE OTHER
	    indices = [np.argwhere(exg['halo_id'] == ID)[0][0] for ID in truth_data['halo_id']]
	    truth_data['m200c'] = np.array([exg['m200c'][i] for i in indices])
	
	return truth_data




## OPEN REDMAPPER CATALOG (BOTH COSMODC2 AND DC2 CATALOGS HAVE SAME STRUCTURE)
def redmapper_cat_open(cat_name, min_richness=0, min_z_cl=0, max_z_cl=1e3) :
	## GET THE CATALOG FROM GCR
	gc = GCRCatalogs.load_catalog(cat_name)
	quantities = gc.list_all_quantities()
	cluster_quantities = [q for q in quantities if 'member' not in q]
	member_quantities = [q for q in quantities if 'member' in q]
	
	## APPLY ANY CONSTRAINTS ON THE DATA
	constraints = [
		f'(richness > {min_richness})',
		f'(redshift > {min_z_cl})',
		f'(redshift < {max_z_cl})',]
	query = GCRCatalogs.GCRQuery(' & '.join(constraints))
	
	cluster_data = Table(gc.get_quantities(cluster_quantities, [query]))
	member_data = Table(gc.get_quantities(member_quantities))
	
	return cluster_data, member_data




## OPEN WAZP COSMODC2 CATALOG
def wazp_cosmoDC2_cat_open(cat_name, min_richness=0, min_z_cl=0, max_z_cl=1e3) :
	## GET THE CATALOG FROM GCR
	gc = GCRCatalogs.load_catalog(cat_name)
	quantities = gc.list_all_quantities()
	cluster_quantities = [q for q in quantities if 'member' not in q]
	member_quantities = [q for q in quantities if 'member' in q]

	## APPLY ANY CONSTRAINTS ON THE DATA
	constraints = [
		f'(cluster_ngals > {min_richness})',
		f'(cluster_z > {min_z_cl})',
		f'(cluster_z < {max_z_cl})',]
	query = GCRCatalogs.GCRQuery(' & '.join(constraints))

	cluster_data = Table(gc.get_quantities(cluster_quantities, [query]))
	member_data  = Table(gc.get_quantities(member_quantities))

	return cluster_data, member_data
