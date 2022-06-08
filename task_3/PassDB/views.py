from .forms import AddPassForm
from .models import Card, Login, Note, AddPass
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from pathlib import Path
import json
import os


class CardListView(generic.ListView):
    model = Card
    template_name = 'card_list.html'
    paginate_by = 5


class CardDetailView(generic.DetailView):
    model = Card
    template_name = 'card_detail.html'


class LoginListView(generic.ListView):
    model = Login
    template_name = 'login_list.html'
    paginate_by = 10


class LoginDetailView(generic.DetailView):
    model = Login
    template_name = 'login_detail.html'


class NoteListView(generic.ListView):
    model = Note
    template_name = 'note_list.html'
    paginate_by = 5


class NoteDetailView(generic.DetailView):
    model = Note
    template_name = 'note_detail.html'


class PassDbListView(generic.ListView):
    model = AddPass
    template_name = 'all_db.html'
    paginate_by = 5


def homepage(request):
    num_cards = Card.objects.all().count()
    num_logins = Login.objects.all().count()
    num_notes = Note.objects.all().count()
    num_db = AddPass.objects.all().count()
    context_data = {'num_cards': num_cards,
                    'num_logins': num_logins,
                    'num_notes': num_notes,
                    'num_db': num_db}
    return render(request, 'home.html', context=context_data)


def add_data(request):
    if request.method == 'POST':
        form = AddPassForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/all_pass_db')
    else:
        form = AddPassForm()
    return render(request, 'entry.html', {'form': form})


def edit_data(request, id):
    try:
        query_data = AddPass.objects.get(id=id)
        if request.method == 'POST':
            query_data.db_label = request.POST.get('db_label')
            query_data.db_date = request.POST.get('db_date')
            query_data.db_path = request.POST.get('db_path')
            query_data.save()
            return HttpResponseRedirect('/all_pass_db')
        else:
            context_data = {'query_data': query_data}
            return render(request, 'edit_data.html', context=context_data)
    except AddPass.DoesNotExist:
        return HttpResponseNotFound('<h2>No data found</h2>')


def delete_data(request, id):
    try:
        query_data = AddPass.objects.get(id=id)
        db_path = str(query_data.db_path)
        delete_file_on_dev(db_path)
        query_data.delete()
    except AddPass.DoesNotExist:
        return HttpResponseNotFound('<h2>No data found</h2>')
    else:
        return HttpResponseRedirect('/all_pass_db')


def delete_file_on_dev(db_path: str) -> None:
    base_dir = Path(__file__).resolve().parent.parent
    path_to_pass_db = os.path.join(base_dir, 'uploads', db_path)
    try:
        os.remove(path_to_pass_db)
    except PermissionError as err:
        HttpResponse(f'<h2>Attention! Deleting completed with an error: {err}.'
                     f'Please close the folder in explorer or another application and try again</h2>')
    except Exception as err:
        HttpResponse(f'<h2>Attention! Deleting completed with an error: {err}</h2>')


def clear_pass(request):
    clear_table_in_db(Card)
    clear_table_in_db(Login)
    clear_table_in_db(Note)
    return HttpResponseRedirect('/')


def search_pass(request):
    label_to_search = None
    if request.method == 'POST':
        label_to_search = request.POST.get('pass_label')
    if label_to_search:
        card_results = search_in_db(Card, label_to_search)
        login_results = search_in_db(Login, label_to_search)
        note_results = search_in_db(Note, label_to_search)
    else:
        card_results = None
        login_results = None
        note_results = None
    label_for_searching = label_to_search
    context_data = {'label_for_searching': label_for_searching,
                    'card_results': card_results,
                    'login_results': login_results,
                    'note_results': note_results}
    return render(request, 'search.html', context=context_data)


def search_in_db(table_name: type, query_text: str) -> list:
    if table_name is Card:
        result_data = table_name.objects.filter(card_name__iregex=query_text)
    elif table_name is Login:
        result_data = table_name.objects.filter(account_name__iregex=query_text)
    else:  # elif table_name is Note:
        result_data = table_name.objects.filter(note_label__iregex=query_text)
    return result_data


def load_pass(request, id):
    try:
        query_data = AddPass.objects.get(id=id)
        base_dir = Path(__file__).resolve().parent.parent
        db_path = str(query_data.db_path)
        path_to_pass_db = os.path.join(base_dir, 'uploads', db_path)
        clear_table_in_db(Card)
        clear_table_in_db(Login)
        clear_table_in_db(Note)
        load_data_from_db(path_to_pass_db)
        db_name = query_data.db_label
        cards_in_db = Card.objects.all().count()
        logins_in_db = Login.objects.all().count()
        notes_in_db = Note.objects.all().count()
        context_data = {'db_name': db_name,
                        'cards_in_db': cards_in_db,
                        'logins_in_db': logins_in_db,
                        'notes_in_db': notes_in_db}
        return render(request, 'load_pass_result.html', context=context_data)
    except Exception as err:
        return HttpResponse(f'<h2>Error! Loading of the passwords completed with an error</h2>'
                            f'<p>{err}</p>')


def clear_table_in_db(table_name: type):
    data_for_delete = table_name.objects.all()
    data_for_delete.delete()


def load_data_from_db(path_to_pass_db: str):
    passwords_data = get_data_from_file(path_to_pass_db)
    cards_data_list, logins_data_list, notes_data_list = create_data_dicts(passwords_data)
    if cards_data_list:
        for input_data in cards_data_list:
            card_data = Card()
            card_data.card_name = input_data['custName']
            card_data.card_number = input_data['cardNumber']
            card_data.card_validity = input_data['expirationDate']
            card_data.card_holder = input_data['holderName']
            card_data.card_cvv = input_data['cvv']
            card_data.card_pin = input_data['pin']
            card_data.card_note = input_data['note']
            card_data.save()
    if logins_data_list:
        for input_data in logins_data_list:
            login_data = Login()
            login_data.account_name = input_data['custName']
            login_data.account_url = input_data['url']
            login_data.account_login = input_data['loginName']
            login_data.account_password = input_data['pwd']
            login_data.account_note = input_data['note']
            login_data.save()
    if notes_data_list:
        for input_data in notes_data_list:
            note_data = Note()
            note_data.note_label = input_data['label']
            note_data.note_text = input_data['text']
            note_data.save()


def get_data_from_file(data_file_path: str) -> dict:
    with open(data_file_path, 'r') as read_file:
        data_pass = json.load(read_file)
    return data_pass


def edit_validity(dict_for_edit: dict) -> dict:
    # 'expirationDate': {'day': D or DD, 'month': M or MM, 'year': YYYY} -> 'DD/YY'
    month = dict_for_edit['expirationDate']['month']
    if month < 10:
        month = '0' + str(month)
    year = dict_for_edit['expirationDate']['year']
    year = str(year)[-2:]
    dict_for_edit['expirationDate'] = f'{month}/{year}'
    return dict_for_edit


def create_data_dicts(input_data: dict) -> list or None:
    cards_data_list = None
    logins_data_list = None
    notes_data_list = None
    if 'cards' in input_data.keys():
        cards_data_list = list()
        for list_element in input_data['cards']:
            cards_data_list.append(edit_validity(list_element))
    if 'logins' in input_data.keys():
        logins_data_list = input_data['logins'].copy()
    if 'notes' in input_data.keys():
        notes_data_list = input_data['notes'].copy()
    return cards_data_list, logins_data_list, notes_data_list
