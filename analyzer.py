"""Analyzer entry. Contains analyze funtion"""
import argparse
import csv
import json
from utils.warnings import AFLearningWarning, FeedbackKnockWarning


def str2bool(v):
    """Map some common truthy/falsy inputs to booleans"""
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


PARSER = argparse.ArgumentParser()
PARSER.add_argument('--log_file', help='Access port data log file to analyze')
PARSER.add_argument('--config_file', help='JSON csv column mapping')
PARSER.add_argument('headers',
                    type=str2bool,
                    nargs='?',
                    const=True,
                    default=True,
                    help='Indicate whether or not the log file has a header row'
                   )


REPORT = {
    'warnings': {
        'feedback_knock': {
            'display': 'Feedback knock levels dropped!',
            'occurrences': []
        },
        'af_learning': {
            'positive': {
                'display': 'ECU is adding a lot of fuel!',
                'occurrences': []
            },
            'negative': {
                'display': 'ECU is pulling a lot of fuel!',
                'occurrences': []
            }
        }
    }
}


def main():
    """Main function"""
    args = PARSER.parse_args()
    log_file = args.log_file
    headers = args.headers
    analyze(log_file, headers)
    report()


def analyze(log_file, headers, config_file='./utils/default_config.json'):
    """Analyzer function"""
    with open(log_file) as log:
        csv_reader = csv.reader(log, delimiter=',')
        # Skip first row if headers are present
        if headers:
            next(csv_reader)

        column_map = None
        with open(config_file) as config:
            column_map = json.load(config)

        for row in csv_reader:
            feedback_knock = row[column_map['feedback_knock']]
            af_learning = row[column_map['AF_learning_1']]
            throttle_pos = row[column_map['throttle_pos']]
            dam = row[column_map['DAM']]
            gear = row[column_map['gear']]
            rpm = row[column_map['RPM']]

            if float(feedback_knock) < 0:
                fbk_warn = FeedbackKnockWarning(feedback_knock, dam, gear, rpm)
                REPORT['warnings']['feedback_knock']['occurrences'].append(fbk_warn)

            if float(af_learning) > 8:
                af_warn = AFLearningWarning(af_learning, throttle_pos, gear, rpm)
                REPORT['warnings']['af_learning']['positive']['occurrences'].append(af_warn)

            if float(af_learning) < -8:
                af_warn = AFLearningWarning(af_learning, throttle_pos, gear, rpm)
                REPORT['warnings']['af_learning']['negative']['occurrences'].append(af_warn)


def report():
    """function used to report back the findings"""
    clean_slate = True
    warnings = REPORT['warnings']
    feedback_knock_warnings = warnings['feedback_knock']['occurrences']
    pos_af_learning_warnings = warnings['af_learning']['positive']['occurrences']
    neg_af_learning_warnings = warnings['af_learning']['negative']['occurrences']

    if feedback_knock_warnings:
        clean_slate = False
        print warnings['feedback_knock']['display']
        print '-----------------------------------------------------'
        print 'Knock Value\tDAM Value\tGear\t\tRPM'
        for warning in feedback_knock_warnings:
            print '{}\t\t{}\t\t{}\t\t{}'.format(warning.knock,
                                                warning.dam,
                                                warning.gear,
                                                warning.rpm
                                               )

    if pos_af_learning_warnings:
        clean_slate = False
        print warnings['af_learning']['positive']['display']
        print '-----------------------------------------------------'
        print 'AF Learning\tThrottle Position\tGear\tRPM'
        for warning in pos_af_learning_warnings:
            print '{}\t\t{}\t\t\t{}\t{}'.format(warning.af_learning,
                                                warning.throttle_pos,
                                                warning.gear,
                                                warning.rpm
                                               )

    if neg_af_learning_warnings:
        clean_slate = False
        print warnings['af_learning']['negative']['display']
        print '-----------------------------------------------------'
        print 'AF Learning\tThrottle Position\tGear\tRPM'
        for warning in neg_af_learning_warnings:
            print '{}\t\t{}\t\t\t{}\t{}'.format(warning.af_learning,
                                                warning.throttle_pos,
                                                warning.gear,
                                                warning.rpm
                                               )

    if clean_slate:
        print 'No warnings to report on! Sweet!'



if __name__ == "__main__":
    main()
