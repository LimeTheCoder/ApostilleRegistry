from django.test import TestCase
from .models import Organ, Department, Signet, Person, Document, DepartmentUser, ApostilleRequest, Apostille
from django.conf import settings
import django.utils
from django.db import IntegrityError
from django.contrib.auth.models import User

class OrganModelTest(TestCase):
	def setUp(self):
		Organ.objects.create(name='Judge', location='New York')
		Organ.objects.create(name='Ministry', location='Kyiv')

	def test_creation(self):
		organ = Organ.objects.get(name='Judge')
		self.assertIsInstance(organ, Organ)

	def test_string_representation(self):
		organ = Organ.objects.get(name='Judge')
		self.assertEqual(str(organ), organ.name)

	def test_pk(self):
		organ = Organ.objects.get(name='Judge')
		self.assertEqual(organ.pk, 1)

	def test_verbose_name_plural(self):
		self.assertEqual(str(Organ._meta.verbose_name_plural), "organs")

	def test_obj_cnt(self):
		self.assertEqual(len(Organ.objects.all()), 2)

	def test_copy(self):
		organ = Organ.objects.get(name='Judge')
		organ.pk = None
		organ.save()
		self.assertEqual(len(Organ.objects.filter(name='Judge')), 2)

	def test_delete_method(self):
		organ = Organ.objects.get(name='Ministry')
		organ.delete()
		try:
			obj = Organ.objects.get(name='Ministry')
		except Organ.DoesNotExist:
			obj = None

		self.assertIsNone(obj)

	def test_update_method(self):
		id = 1
		organ = Organ.objects.get(pk=id)
		organ.name='High School'
		organ.save()
		updated_org = Organ.objects.get(name='High School')
		self.assertEqual(updated_org.id, id)




class DepartmentModelTest(TestCase):
	def setUp(self):
		organ = Organ.objects.create(name='Judge', location='New York')
		organ2 = Organ.objects.create(name='Ministry', location='Kyiv')
		
		Department.objects.create(organ=organ)
		Department.objects.create(organ=organ2)

	def test_creation(self):
		department = Department.objects.get(organ__name='Judge')
		self.assertIsInstance(department, Department)

	def test_string_representation(self):
		department = Department.objects.get(organ__name='Judge')
		self.assertEqual(str(department), department.organ.name)

	def test_pk(self):
		department = Department.objects.get(organ__name='Judge')
		self.assertEqual(department.pk, 1)

	def test_verbose_name_plural(self):
		self.assertEqual(str(Department._meta.verbose_name_plural), "departments")

	def test_default_icon(self):
		department = Department.objects.get(organ__name='Judge')
		self.assertEqual(department.icon, settings.MEDIA_URL + '/apostille.jpg')

	def test_obj_cnt(self):
		self.assertEqual(len(Department.objects.all()), 2)

	def test_delete_method(self):
		department = Department.objects.get(organ__name='Ministry')
		department.delete()
		try:
			obj = Department.objects.get(organ__name='Ministry')
		except Department.DoesNotExist:
			obj = None

		try:
			org = Organ.objects.get(name='Ministry')
		except Organ.DoesNotExist:
			org = None

		self.assertIsNone(obj)
		self.assertIsNotNone(org)

	def test_update_method(self):
		id = 1
		department = Department.objects.get(pk=id)
		organ = Organ.objects.create(name='School', location='London')

		department.organ = organ
		department.save()
		updated_obj = Department.objects.get(organ__name='School')
		self.assertEqual(updated_obj.id, id)

	def test_one_to_one_rel(self):
		department = Department.objects.get(pk=1)
		organ = department.organ
		try:
			obj = Department.objects.create(organ=organ)
		except IntegrityError:
			obj = None

		self.assertIsNone(obj)


	def test_delete_cascade(self):
		try:
			department = Department.objects.get(organ__name='Judge')
		except Department.DoesNotExist:
			department = None
		
		self.assertIsNotNone(department) # is not None before foreign key delete
		
		id = department.id

		organ = Organ.objects.get(name='Judge')
		organ.delete()

		try:
			department = Department.objects.get(pk=id)
		except Department.DoesNotExist:
			department = None
		
		self.assertIsNone(department)


class SignetModelTest(TestCase):
	def setUp(self):
		self.path = settings.MEDIA_URL + '/16.17.jpg'
		self.path2 = settings.MEDIA_URL + '/16.22.jpg'

		Signet.objects.create(sign=self.path)
		Signet.objects.create(stamp=self.path2)

	def test_creation(self):
		signet = Signet.objects.get(sign=self.path)
		self.assertIsInstance(signet, Signet)

	def test_string_representation(self):
		signet = Signet.objects.get(sign=self.path)
		self.assertEqual(str(signet), 'Signet #1')

	def test_pk(self):
		signet = Signet.objects.get(sign=self.path)
		self.assertEqual(signet.pk, 1)

	def test_verbose_name_plural(self):
		self.assertEqual(str(Signet._meta.verbose_name_plural), "signets")

	def test_nullable_stamp(self):
		signet = Signet.objects.get(sign=self.path)
		self.assertFalse(signet.stamp)

	def test_obj_cnt(self):
		self.assertEqual(len(Signet.objects.all()), 2)

	def test_copy(self):
		signet = Signet.objects.get(sign=self.path)
		signet.pk = None
		signet.save()
		self.assertEqual(len(Signet.objects.filter(sign=self.path)), 2)

	def test_delete_method(self):
		signet = Signet.objects.get(stamp=self.path2)
		signet.delete()
		try:
			obj = Signet.objects.get(stamp=self.path2)
		except Signet.DoesNotExist:
			obj = None

		self.assertIsNone(obj)

	def test_update_method(self):
		id = 1
		signet = Signet.objects.get(pk=id)
		new_sign = settings.MEDIA_URL + '/16.26.jpg'
		signet.sign = new_sign
		signet.save()
		updated_obj = Signet.objects.get(sign=new_sign)
		self.assertEqual(updated_obj.id, id)


class PersonModelTest(TestCase):
	def setUp(self):

		self.path = settings.MEDIA_URL + '/16.17.jpg'
		self.path2 = settings.MEDIA_URL + '/16.22.jpg'

		signet1 = Signet.objects.create(sign=self.path)
		signet2 = Signet.objects.create(stamp=self.path2)

		organ1 = Organ.objects.create(name='City Hall', location='New York')
		organ2 = Organ.objects.create(name='Ministry', location='Kyiv')

		Person.objects.create(name='Oleg', surname='Ivanov', patronymic='Olexandrovich',
								 location='New York', job_start_date=django.utils.timezone.now(),
								 position='Mayor', signet=signet1, organ=organ1)

		Person.objects.create(name='Andriy', surname='Semenko', patronymic='Ivanovich',
								 location='Kyiv', job_start_date=django.utils.timezone.now(),
								 position='Minister', signet=signet2, organ=organ2)

	def test_creation(self):
		person = Person.objects.get(pk=1)
		self.assertIsInstance(person, Person)

	def test_string_representation(self):
		person = Person.objects.get(pk=1)
		self.assertEqual(str(person), (person.name + " " + person.surname))

	def test_pk(self):
		person = Person.objects.get(name='Oleg', surname='Ivanov')
		self.assertEqual(person.pk, 1)

	def test_verbose_name_plural(self):
		self.assertEqual(str(Person._meta.verbose_name_plural), "persons")

	def test_obj_cnt(self):
		self.assertEqual(len(Person.objects.all()), 2)

	def test_nullable_date(self):
		person = Person.objects.get(pk=1)
		self.assertFalse(person.job_finish_date)

	def test_delete_method(self):
		person = Person.objects.get(name='Andriy', surname='Semenko')
		person.delete()
		
		try:
			obj = Person.objects.get(name='Andriy', surname='Semenko')
		except Person.DoesNotExist:
			obj = None

		self.assertIsNone(obj)

	def test_update_method(self):
		id = 1
		person = Person.objects.get(pk=id)
		organ = Organ.objects.create(name='School', location='London')

		person.organ = organ
		person.save()
		updated_obj = Person.objects.get(organ__name='School')
		self.assertEqual(updated_obj.id, id)

	def test_one_to_one_rel(self):
		person = Person.objects.get(pk=1)
		signet = person.signet
		try:
			organ = Organ.objects.get(name='Ministry')
			obj = Person.objects.create(name='Volodymyr', surname='Kovalenko', 
					patronymic='Maximovych',location='Kharkiv', 
					job_start_date=django.utils.timezone.now(),
					position='Minister', signet=signet, organ=organ)
		except IntegrityError:
			obj = None

		self.assertIsNone(obj)


	def test_foreign_key(self):
		person = Person.objects.get(pk=1)
		organ = person.organ
		try:
			signet = Signet.objects.create()
			obj = Person.objects.create(name='Volodymyr', surname='Kovalenko', 
					patronymic='Maximovych',location='Kharkiv', 
					job_start_date=django.utils.timezone.now(),
					position='Minister', signet=signet, organ=organ)
		except IntegrityError:
			obj = None

		self.assertIsNotNone(obj)

	def test_delete_cascade(self):
		try:
			person = Person.objects.get(organ__name='City Hall')
		except Person.DoesNotExist:
			person = None
		
		self.assertIsNotNone(person) # is not None before foreign key delete
		
		id = person.id

		organ = Organ.objects.get(name='City Hall')
		organ.delete()

		try:
			person = Person.objects.get(pk=id)
		except Person.DoesNotExist:
			person = None
		
		self.assertIsNone(person)


class DocumentModelTest(TestCase):
	def setUp(self):
		Document.objects.create(name='Goverment Document', issue_date=django.utils.timezone.now(),
					 file=settings.MEDIA_URL+'/document.txt', signer_name='George',
					 signer_surname='Lewis')
		
		Document.objects.create(name='Secret Document', issue_date=django.utils.timezone.now(),
					 file=settings.MEDIA_URL+'/document.txt', signer_name='Oleg',
					 signer_surname='Ivanov', signer_patronymic='Maximovych')

	def test_creation(self):
		document = Document.objects.get(name='Secret Document')
		self.assertIsInstance(document, Document)

	def test_string_representation(self):
		document = Document.objects.get(name='Secret Document')
		self.assertEqual(str(document), document.name)

	def test_pk(self):
		document = Document.objects.get(name='Goverment Document')
		self.assertEqual(document.pk, 1)

	def test_verbose_name_plural(self):
		self.assertEqual(str(Document._meta.verbose_name_plural), "documents")

	def test_obj_cnt(self):
		self.assertEqual(len(Document.objects.all()), 2)

	def test_copy(self):
		document = Document.objects.get(name='Goverment Document')
		document.pk = None
		document.save()
		self.assertEqual(len(Document.objects.filter(name='Goverment Document')), 2)

	def test_delete_method(self):
		document = Document.objects.get(name='Secret Document')
		document.delete()
		try:
			obj = Document.objects.get(name='Secret Document')
		except Document.DoesNotExist:
			obj = None

		self.assertIsNone(obj)

	def test_update_method(self):
		id = 1
		document = Document.objects.get(pk=id)
		document.name='Education document'
		document.save()
		updated_doc = Document.objects.get(name='Education document')
		self.assertEqual(updated_doc.id, id)


class DepartmentUserModelTest(TestCase):
	def setUp(self):
		organ1 = Organ.objects.create(name='City Hall', location='New York')
		organ2 = Organ.objects.create(name='Ministry', location='Kyiv')

		department1 = Department.objects.create(organ=organ1)
		department2 = Department.objects.create(organ=organ2)

		user1 = User.objects.create_user(username='john',
                                 email='jlennon@beatles.com',
                                 password='glass onion')

		user2 = User.objects.create_user(username='jack',
                                 email='jack@notbeatles.com',
                                 password='password')

		DepartmentUser.objects.create(user=user1, department=department1)
		DepartmentUser.objects.create(user=user2, department=department2)



	def test_creation(self):
		dep_user = DepartmentUser.objects.get(pk=1)
		self.assertIsInstance(dep_user, DepartmentUser)

	def test_string_representation(self):
		dep_user = DepartmentUser.objects.get(pk=1)
		self.assertEqual(str(dep_user), dep_user.user.username)

	def test_pk(self):
		dep_user = DepartmentUser.objects.get(user__username='jack')
		self.assertEqual(dep_user.pk, 2)

	def test_verbose_name_plural(self):
		self.assertEqual(str(DepartmentUser._meta.verbose_name_plural), "department users")
		
	def test_obj_cnt(self):
		self.assertEqual(len(DepartmentUser.objects.all()), 2)

	def test_delete_method(self):
		user = DepartmentUser.objects.get(user__username='jack')
		user.delete()
		
		try:
			obj = DepartmentUser.objects.get(user__username='jack')
		except DepartmentUser.DoesNotExist:
			obj = None

		self.assertIsNone(obj)

	def test_update_method(self):
		id = 1
		duser = DepartmentUser.objects.get(pk=id)
		
		user = User.objects.create_user(username='jessy',
                                 email='jjj@gmail.com',
                                 password='password')

		duser.user = user
		duser.save()
		updated_obj = DepartmentUser.objects.get(user__username='jessy')
		self.assertEqual(updated_obj.id, id)


	def test_one_to_one_rel(self):

		department = Department.objects.get(organ__name='City Hall')

		user = User.objects.create_user(username='mary',
                                 email='mary@gmail.com',
                                 password='mary27')
		try:

			obj = DepartmentUser.objects.create(user=user, department=department)
		except IntegrityError:
			obj = None
		self.assertIsNone(obj)

	def test_delete_cascade(self):
		try:
			dep_user = DepartmentUser.objects.get(department__organ__name='City Hall')
		except Person.DoesNotExist:
			dep_user = None
		
		self.assertIsNotNone(dep_user) # is not None before foreign key delete
		
		id = dep_user.id

		organ = Organ.objects.get(name='City Hall')
		organ.delete()

		try:
			dep_user = DepartmentUser.objects.get(pk=id)
		except DepartmentUser.DoesNotExist:
			dep_user = None
		
		self.assertIsNone(dep_user)


class ApostilleRequestModelTest(TestCase):
	def setUp(self):
		organ = Organ.objects.create(name='City Hall', location='New York')
		organ2 = Organ.objects.create(name='Ministry', location='Kyiv')

		department = Department.objects.create(organ=organ)
		department2 = Department.objects.create(organ=organ2)

		user = User.objects.create_user(username='john',
                                 email='jlennon@beatles.com',
                                 password='glass onion')

		user2 = User.objects.create_user(username='mary',
                                 email='mary@gmail.com',
                                 password='mary27')

		dep_user = DepartmentUser.objects.create(user=user, department=department)
		dep_user2 = DepartmentUser.objects.create(user=user2, department=department2)

		doc = Document.objects.create(name='Goverment Document', issue_date=django.utils.timezone.now(),
					 file=settings.MEDIA_URL+'/document.txt', signer_name='George',
					 signer_surname='Lewis')

		doc2 = Document.objects.create(name='Secret Document', issue_date=django.utils.timezone.now(),
					 file=settings.MEDIA_URL+'/document.txt', signer_name='Oleg',
					 signer_surname='Ivanov', signer_patronymic='Maximovych')

		ApostilleRequest.objects.create(document=doc, user=dep_user, payment_file=settings.MEDIA_URL+'/document.txt')
		ApostilleRequest.objects.create(document=doc2, user=dep_user2, payment_file=settings.MEDIA_URL+'/document.txt')

	def test_creation(self):
		req = ApostilleRequest.objects.get(pk=1)
		self.assertIsInstance(req, ApostilleRequest)

	def test_string_representation(self):
		req = ApostilleRequest.objects.get(pk=1)
		self.assertEqual(str(req), req.document.name)

	def test_pk(self):
		req = ApostilleRequest.objects.get(document__name='Goverment Document')
		self.assertEqual(req.pk, 1)

	def test_verbose_name_plural(self):
		self.assertEqual(str(ApostilleRequest._meta.verbose_name_plural), "apostille requests")
		
	def test_obj_cnt(self):
		self.assertEqual(len(ApostilleRequest.objects.all()), 2)

	def test_delete_method(self):
		req = ApostilleRequest.objects.get(document__name='Secret Document')
		req.delete()
		
		try:
			obj = ApostilleRequest.objects.get(document__name='Secret Document')
		except ApostilleRequest.DoesNotExist:
			obj = None

		self.assertIsNone(obj)

	def test_update_method(self):
		id = 1
		req = ApostilleRequest.objects.get(pk=id)
		
		user = User.objects.create_user(username='mia',
                                 email='jjj@gmail.com',
                                 password='password')

		req.user.user = user
		req.user.save()
		updated_obj = ApostilleRequest.objects.get(user__user__username='mia')
		self.assertEqual(updated_obj.id, id)


	def test_one_to_one_rel(self):

		doc = Document.objects.get(name='Goverment Document')

		user = User.objects.create_user(username='mike',
                                 email='mary@gmail.com',
                                 password='mary27')


		organ = Organ.objects.create(name='School', location='Lviv')
		department = Department.objects.create(organ=organ)
		dep_user = DepartmentUser.objects.create(user=user, department=department)

		try:

			obj = ApostilleRequest.objects.create(user=dep_user, document=doc, payment_file=settings.MEDIA_URL+'/document.txt')
		except IntegrityError:
			obj = None
		self.assertIsNone(obj)

	def test_foreign_key(self):

		dep_user = DepartmentUser.objects.get(user__username='john')

		doc = Document.objects.create(name='Test Document', issue_date=django.utils.timezone.now(),
					 file=settings.MEDIA_URL+'/document.txt', signer_name='George',
					 signer_surname='Lewis')


		try:
			obj = ApostilleRequest.objects.create(document=doc, user=dep_user, payment_file=settings.MEDIA_URL+'/document.txt')
		except IntegrityError:
			obj = None

		self.assertIsNotNone(obj)

	def test_delete_cascade(self):
		try:
			req = ApostilleRequest.objects.get(document__name='Goverment Document')
		except Person.DoesNotExist:
			req = None
		
		self.assertIsNotNone(req) # is not None before foreign key delete
		
		id = req.id

		document = Document.objects.get(name='Goverment Document')
		document.delete()

		try:
			req = ApostilleRequest.objects.get(pk=id)
		except ApostilleRequest.DoesNotExist:
			req = None
		
		self.assertIsNone(req)