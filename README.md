# ECS-Schema-Validator
Proof of concept for a ECS schema based field searcher, potentially a validator in the future

# Quick Start
1. run ```sh setup.sh``` to setup the POC
2. hit the api endpoint to get the results ```curl http://127.0.0.1:8000/field-query?field=geo```]
3. results should be like
  ```JSONasPython
  [{"score":4.373568,"Field":"threat.indicator.geo.country_iso_code","Description":"Country ISO code.","Field_Set":"threat","Level":"core"},{"score":4.373568,"Field":"threat.indicator.geo.country_name","Description":"Country name.","Field_Set":"threat","Level":"core"},{"score":4.373568,"Field":"threat.indicator.geo.location","Description":"Longitude and latitude.","Field_Set":"threat","Level":"core"},{"score":4.373568,"Field":"threat.indicator.geo.name","Description":"User-defined description of a location.","Field_Set":"threat","Level":"extended"},{"score":4.373568,"Field":"threat.indicator.geo.postal_code","Description":"Postal code.","Field_Set":"threat","Level":"core"},{"score":4.373568,"Field":"threat.indicator.geo.region_iso_code","Description":"Region ISO code.","Field_Set":"threat","Level":"core"},{"score":4.373568,"Field":"threat.indicator.geo.region_name","Description":"Region name.","Field_Set":"threat","Level":"core"},{"score":4.373568,"Field":"threat.indicator.geo.timezone","Description":"Time zone.","Field_Set":"threat","Level":"core"},{"score":4.373568,"Field":"threat.indicator.geo.city_name","Description":"City name.","Field_Set":"threat","Level":"core"},{"score":4.373568,"Field":"threat.indicator.geo.continent_code","Description":"Continent code.","Field_Set":"threat","Level":"core"}]
  ```
