from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from assets.models import Asset, Asset_User_Mapping
from .models import Booking
from .forms import BookingForm
from myfunctions import get_owners_and_dates

import datetime

@login_required(login_url='/login/')
def my_bookings(request):
    my_id = request.user
    my_bookings = Booking.objects.all().filter(requested_by_user_ID=my_id)
    return render(request, "bookings.html", {"bookings": my_bookings})

@login_required(login_url='/login/')
def all_future_asset_bookings(request, asset_id, for_user=0):
    the_asset = get_object_or_404(Asset, pk=asset_id)

    # optional userID
    if for_user == 0:
        all_bookings = Booking.objects.all().filter(asset_ID=the_asset).filter(start_date__gt=datetime.date.today())
    else:
        my_id = request.user
        all_bookings = Booking.objects.all().filter(asset_ID=the_asset).filter(requested_by_user_ID=my_id,
                                                                               start_date__gt=datetime.date.today())

    return render(request, "all_bookings.html", {"asset": the_asset, "all_bookings": all_bookings})

@login_required(login_url='/login/')
def booking_detail(request, booking_id):
    the_booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, "booking_detail.html",{"booking": the_booking})

def get_owner_id_NOT_USED(the_asset, the_start_date, the_end_date):

    the_asset = Asset.objects.get(pk=the_asset)
    share_start_date = the_asset.sharing_start_date
    slot_duration = the_asset.slot_duration_unit.duration_type
    num_durations = the_asset.number_of_slot_units

    if the_asset.sharing_with_other_owners:

        the_owners = Asset_User_Mapping.objects.all().filter(asset_ID=the_asset.id,is_owner=True)

        if the_owners.count > 1:

            # find out which one is the owner on the DATES given
            # next line just temporary for testing
            owner_id = the_owners[0].user_ID

        else:
            owner_id = the_owners[0].user_ID #or just user_ID (for email)

    return owner_id


@login_required(login_url='/login/')
def make_a_booking(request, asset_id):

    the_asset = get_object_or_404(Asset, pk=asset_id)
    errors = []
    owner_date_object = []
    total_days_requested = 0

    if request.method == "POST":
        new_booking_form = BookingForm(request.POST)
        if new_booking_form.is_valid():

            #save it in memory while getting the addition info need to save it to the database
            new_booking = new_booking_form.save(False)
            new_booking.asset_ID_id = the_asset.id
            new_booking.requested_by_user_ID = request.user

            owner_id = get_owner_id(new_booking.asset_ID_id,new_booking.start_date, new_booking.end_date)

            new_booking.slot_owner_id = owner_id
            #now save to database

            new_booking.save()

            # booking_id = models.AutoField(primary_key=True)
            # asset_ID = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="asset_booked")
            # requested_by_user_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
            #                                          related_name="requested_by")
            # slot_owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
            # start_date = models.DateField(blank=False)
            # end_date = models.DateField(blank=False)
            # is_confirmed = models.BooleanField(default=False)
            # deposit_paid = models.BooleanField(default=False)
            # date_created = models.DateTimeField(default=timezone.now)

            messages.success(request, "New Booking created, thanks")
            return redirect(reverse('booking_detail', args={new_booking.pk}))

    else:


        #request.method is GET,
        #check which stage of get
        if 'start_date' in request.GET:
            start_date = request.GET['start_date']
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

            if 'end_date' in request.GET:
                end_date = request.GET['end_date']
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

            if end_date.toordinal() - start_date.toordinal() < 0:
                errors.append('Your end date is earlier than your start date - please correct!')

                new_booking_form = BookingForm(request.GET)

            else:
                # dates are fine (unless I programme more validation) so now continue with
                # displaying the ownership for the date range!
                owner_date_object = get_owners_and_dates(asset_id, start_date, end_date)
                for item in owner_date_object:
                    total_days_requested += item.days_requested

                new_booking_form = BookingForm(request.GET)

        else:
            # this is first time so just display the form
            new_booking_form = BookingForm()

    args = {
        'booking_form': new_booking_form,
        'the_asset': the_asset,
        'errors': errors,
        'owner_date_object': owner_date_object,
        'total_days_requested': total_days_requested,
    }

    args.update(csrf(request))

    return render(request, "new_booking.html", args)



