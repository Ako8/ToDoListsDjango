from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from register.forms import RegisterForm
# Create your views here.


def index(response, id):
	ls = ToDoList.objects.get(id=id)

	if response.method == "POST": 
		if response.POST.get("save"):
			for item in ls.item_set.all():
				if response.POST.get(str(item.id)) == "clicked":
					item.complete = True
				else:
					item.complete = False
				item.save()
		elif response.POST.get("newItem"):
			txt = response.POST.get("new")
			allitem = [str(ite) for ite in ls.item_set.all()]

			if len(txt) > 2 and not txt in allitem:
				ls.item_set.create(text=txt, complete=False)

		elif response.POST.get("delete"):
			for obj in ls.item_set.all():
				# if response.POST.get(str(obj.id)) == "clicked":
				if obj.complete:
					ls.item_set.get(text=str(obj)).delete()

					


	return render(response, "main/list.html", {"ls":ls})


def home(response):
	return render(response, "main/home.html", {})
	

def create(response):
	if response.method == "POST":
		form = CreateNewList(response.POST)
		lsofls = [str(ls) for ls in ToDoList.objects.all()]

		if form.is_valid():
			n = form.cleaned_data["name"]
			if not n in lsofls:
				t = ToDoList(name=n)
				t.save()
				return HttpResponseRedirect("/%i" %t.id)
	else:
		form = CreateNewList()
	return render(response, "main/create.html", {"form":form})


def lists(response):
	lss = ToDoList.objects.all()
	return render(response, "main/todolists.html", {"ls":lss})