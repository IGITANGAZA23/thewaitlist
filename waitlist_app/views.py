from django.shortcuts import render, redirect, get_object_or_404
from .models import WaitlistEntry
from .forms import WaitlistEntryForm

# 1. READ (List all waitlist entries)
def waitlist_list(request):
    entries = WaitlistEntry.objects.all()
    return render(request, 'waitlist_app/waitlist_list.html', {'entries': entries})

# 2. CREATE (Join the waitlist)
def waitlist_create(request):
    if request.method == 'POST':
        form = WaitlistEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('waitlist_list')
    else:
        form = WaitlistEntryForm()
    return render(request, 'waitlist_app/waitlist_form.html', {'form': form, 'action': 'Join'})

# 3. UPDATE (Edit waitlist entry)
def waitlist_update(request, pk):
    entry = get_object_or_404(WaitlistEntry, pk=pk)
    if request.method == 'POST':
        form = WaitlistEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('waitlist_list')
    else:
        form = WaitlistEntryForm(instance=entry)
    return render(request, 'waitlist_app/waitlist_form.html', {'form': form, 'action': 'Update'})

# 4. DELETE (Remove from waitlist)
def waitlist_delete(request, pk):
    entry = get_object_or_404(WaitlistEntry, pk=pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('waitlist_list')
    return render(request, 'waitlist_app/waitlist_confirm_delete.html', {'entry': entry})
