import scrappers
import dynamodb

terms = ['Python', 'SQL', 'React', 'Angular', 'JavaScript', 'Java', 'aws', 'Node', 'Docker']

platforms_dict = {
    #'linkedin': ['ar', 'br', 'cl', 'ec', 'co', 'cr', 'pa', 'pe', 'mx'],
    'computrabajo': ['ar', 'ec', 'co', 'pa', 'pe', 'mx'],
    'indeed': ['ar', 'br', 'cl', 'ec', 'co', 'cr', 'pa', 'pe', 'mx'],
    'opcionempleo': ['ar', 'ec', 'co', 'cr', 'pa', 'pe', 'mx']
}

functions_dict = {
    'linkedin': scrappers.get_jobs_num_linkedin,
    'computrabajo': scrappers.get_jobs_num_computrabajo,
    'indeed': scrappers.get_jobs_num_indeed,
    'opcionempleo': scrappers.get_jobs_num_opcionempleo
}

def run_scrappers(test = False):
    for term in terms:
        for platform in platforms_dict:
            for country in platforms_dict[platform]:
                try:
                    result_dict = functions_dict[platform](term, country)
                    for item in result_dict:
                        identifier = term +'.'+ platform + '.' + country + '.' + item
                        jobs_num = str(result_dict[item])
                        if test:
                            print (term +' '+ platform + ' ' + country + ' ' + str(result_dict[item]))
                        else:
                            result = dynamodb.add_to_table(identifier, jobs_num)
                            if result['ResponseMetadata']['HTTPStatusCode'] != 200:
                                print('Error in ' + term +' '+ platform + ' ' + country)
                except:
                    print('Error in ' + term +' '+ platform + ' ' + country)
                    continue

if __name__ == '__main__':
    run_scrappers(test = True)