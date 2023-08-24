import os
os.getcwd()
os.chdir('/home/method/Research/Sam/VA/CountrySupport/Rwanda/2022-08-10')
os.listdir('.')

import openva_pipeline as ovapl
# ovapl.create_transfer_db("pipeline.db", ".", "rwanda")
pl = ovapl.Pipeline(db_file_name="pipeline.db",
                    db_directory=".",
                    db_key="rwanda",
                    use_dhis="True")
# pl._update_dhis(["dhisURL", "dhisUser", "dhisPassword", "dhisOrgUnit"],
#                 ["https://ncd.rbc.gov.rw/testindividualrecords",
#                  "verbalautopsy",
#                  "Verbal@2020",
#                  "WqBWirWKNao"])
# pl._get_dhis_conf()

#settings = pl.config()
#dhis_out = pl.run_dhis(settings)
pl.store_results_db()