import os
import xnat
import random
import string


class XnatClient(object):

    def __init__(self, host, user, password, project_id, test_run=True):
        if not host.startswith('http'):
            host = 'https://' + host
        self._session = xnat.connect(host, user=user, password=password)
        self._project = self._session.projects[project_id]
        self._test_run = test_run
        print('Loaded project {} containing {} subjects'.format(self._project.id, len(self._project.subjects)))

    def project(self):
        return self._project

    def create_project(self, project_id, project_name):
        project = None
        if project_id not in self._session.projects.keys():
            if self._test_run:
                print('Creating project {}'.format(project_id))
            else:
                project = self._session.classes.ProjectData(parent=self._session, label=project_id, name=project_name)
        else:
            print('Retrieving project {}'.format(project_id))
            project = self._session.projects[project_id]
        return project

    def subjects(self):
        return self._project.subjects.data.values()

    def subject(self, subject_id):
        return self._project.subjects[subject_id]

    def create_subject(self, subject_id):
        subject = None
        if subject_id not in self._project.subjects.keys():
            if self._test_run:
                print('Creating subject {}'.format(subject_id))
            else:
                subject = self._session.classes.SubjectData(parent=self._project, label=subject_id)
        else:
            print('Retrieving subject {}'.format(subject_id))
            subject = self._project.subjects[subject_id]
        return subject

    def delete_project(self, project_id):
        project = self._session.projects[project_id]
        self.delete_all_subjects(project)
        project.delete()

    def delete_subject(self, subject, verbose=True):
        subject_id = subject.label
        if self._test_run and verbose:
            print('Deleting subject {}'.format(subject.label))
        else:
            experiments = subject.experiments.data.values()
            for experiment in experiments:
                experiment.delete()
            subject.delete()
            if verbose:
                print('Deleted subject {}'.format(subject_id))

    def delete_all_subjects(self, project):
        subjects = project.subjects.data.values()
        count = 0
        for subject in subjects:
            self.delete_subject(subject, verbose=False)
            print('Deleted subject {}/{}'.format(count, len(subjects)))
            count += 1

    def create_experiment(self, experiment_id, subject):
        # Experiment ID must be unique within whole project so prepend with subject ID
        experiment_id = '{}_{}'.format(subject.label, experiment_id)
        experiment = None
        if self._test_run:
            print('Creating experiment {}'.format(experiment_id))
        else:
            if experiment_id not in subject.experiments.keys():
                experiment = self._session.classes.CtSessionData(parent=subject, label=experiment_id)
            else:
                print('Retrieving experiment {}'.format(experiment_id))
                experiment = subject.experiments[experiment_id]
        return experiment

    def create_resource_folder(self, resource_folder_id, experiment):
        # Resource folder ID needs to be unique only within experiment. Within this resource
        # folder you can upload multiple resource files.
        resource = None
        if resource_folder_id not in experiment.resources.keys():
            if self._test_run:
                print('Creating resource folder {}'.format(resource_folder_id))
            else:
                resource = self._session.classes.ResourceCatalog(parent=experiment, label=resource_folder_id)
        else:
            print('Retrieving resource folder {}'.format(resource_folder_id))
            resource = experiment.resources[resource_folder_id]
        return resource

    def upload_resource(self, file_path, subject_id, experiment_id, resource_folder_id, overwrite=True):
        subject = self.subject(subject_id)
        experiment = subject.experiments[experiment_id]
        resource = self.create_resource_folder(resource_folder_id, experiment)
        if self._test_run:
            print('Uploading resource {} to resource folder {} of experiment {} for subject {} in project {}'.format(
                file_path,
                resource_folder_id,
                experiment_id,
                subject_id, self._project.id))
        else:
            resource.upload(file_path, os.path.split(file_path)[1], overwrite=overwrite)
            print('Uploaded resource {} to resource folder {} of experiment {} for subject {} in project {}'.format(
                file_path,
                resource_folder_id,
                experiment_id,
                subject_id, self._project.id))

    def share_experiments(self, experiment_ids, target_project_id):
        if ' ' in target_project_id:
            raise RuntimeError('Target project ID cannot contain spaces!')
        # Get target project object
        random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        target_project_id = '{}_{}'.format(target_project_id, random_id)
        target_project = self.create_project(target_project_id, target_project_id)
        # Run through list of experiment IDs
        for experiment_id in experiment_ids:
            # Get subject ID from experiment ID which has format <subjectId>_<experimentName>
            subject_id = experiment_id.split('_')[0]
            # Share subject. You must do this otherwise the shared experiment will not be visible
            # in the target project
            if subject_id not in self._project.subjects.keys():
                raise RuntimeError('Subject {} does not exist in source project'.format(subject_id))
            subject = self.subject(subject_id)
            if self._test_run:
                print('Sharing subject {} with target project {}'.format(subject_id, target_project_id))
                print('Sharing subject {} experiments {}'.format(subject_id, experiment_id))
            else:
                # If the subject has already been shared with the target project, skip this step
                if subject_id in target_project.subjects.keys():
                    print('Subject {} has already been shared with target project'.format(subject_id))
                else:
                    subject.share(target_project_id, label=subject_id)
                    print('Shared subject {} with project {}'.format(subject_id, target_project_id))
                # Share experiment
                if experiment_id not in subject.experiments.keys():
                    raise RuntimeError('Experiment {} does not exist in source project'.format(experiment_id))
                experiment = subject.experiments[experiment_id]
                # If the experiment has already been shared with the target project, skip this step
                if experiment_id in target_project.experiments.keys():
                    print('Experiment {} has already been shared with target project'.format(experiment_id))
                else:
                    experiment.share(target_project_id, label=experiment_id)
                    print('Shared experiment {} of subject {} with project {}'.format(experiment_id, subject_id, target_project_id))
        return target_project_id
