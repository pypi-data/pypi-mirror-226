from astroquery.sdss import SDSS
from astroquery.exceptions import RemoteServiceError
from requests.exceptions import ConnectionError
from astropy.table import Table
import numpy as np


# Esse é um módulo Python feito por mim @aCosmicDebbuger
# https://github.com/aCosmicDebugger
# Neste módulo uso o astroquery do astropy para fazer uma query
# dos dados do SDSS (release 17)  contendo a natureza do objeto
# o redshift, declinação e acendência e os fluxos nas bandas u,g,r,i



def query_sdss_data():
    try:
        # query SDSS database e pedindo os rótulos spaceobjid, ra, dec, z, fluxo banda u, i, r, e z.
        query = """
        SELECT
            s.specobjid, s.ra, s.dec, s.z, s.class, p.flux_u, p.flux_g, p.flux_r, p.flux_i, p.flux_z
        FROM
            specObj s
        JOIN
            photoObjAll p ON s.bestObjID = p.objID
        WHERE
            s.z > 0 AND s.zWarning = 0
        """
        
        # o restulado da query é recebido por result
        result = SDSS.query_sql(query)
        
        # caso apareça algum valor NaN nas colunas de fluxo
        flux_columns = ['flux_u', 'flux_g', 'flux_r', 'flux_i', 'flux_z']
        for column in flux_columns:
            result[column] = np.nan_to_num(result[column])
            
        return result
    except RemoteServiceError as e:
        print("Erro ao fazer o querying SDSS:", e)
        return None
    except ConnectionError as e:
        print("Erro de conexão:", e)
        return None

if __name__ == "__main__":
    # Fazendo o query
    sdss_data = query_sdss_data()
    
    if sdss_data is not None:
        # printando os dados
        print(sdss_data)
    else:
        print("Error retrieving SDSS data.")

