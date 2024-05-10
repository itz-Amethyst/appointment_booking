from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin , CreateModelMixin , RetrieveModelMixin , DestroyModelMixin , \
    UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_framework.permissions import IsAuthenticated


from appointment_booking.api.serializers import CreateBookingSerializer, BookingWithoutUserCredentialsSerializer
from appointment_booking.models import OrderItem


class BookingViewSet(GenericViewSet , ListModelMixin , CreateModelMixin , RetrieveModelMixin , UpdateModelMixin ,
                    DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post", "delete"]

    def get_serializer_context( self ):
        return {"request": self.request , "user": self.request.user}

    def get_serializer_class( self ):
        if self.request.method == "POST" and self.request.user.is_authenticated:
            return BookingWithoutUserCredentialsSerializer
        elif self.request.method == "POST":
            return CreateBookingSerializer

    def create( self , request , *args , **kwargs ):
        """
        Handle the POST request to create a booking with a new user.
        """
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        booking = serializer.save()  # Create the booking and the user

        return Response(
            {
                "message": "Booking created successfully." ,
                "booking": {
                    "start_time": booking.start_time ,
                    "end_time": booking.end_time ,
                    "booked_by": booking.booked_by.username ,
                } ,
            } ,
            status = status.HTTP_201_CREATED ,
        )

    @action(detail = False , methods = ["delete"] , url_path = "cancel-by-code")
    def cancel_by_reservation_code( self , request , *args , **kwargs ):
        """
        Custom DELETE endpoint to cancel a booking based on `reservation_code`.
        """
        # Get the reservation code from the request data
        reservation_code = request.data.get("reservation_code")

        if not reservation_code:
            return Response(
                {"error": "Reservation code is required."} ,
                status = status.HTTP_400_BAD_REQUEST
            )

        # Find the OrderItem with the given reservation code
        order_item = get_object_or_404(OrderItem , reservation_code = reservation_code)

        # Find the associated Booking
        booking = order_item.booking_id  # Get the associated Booking

        # Set `is_canceled` to true
        booking.is_canceled = True
        booking.save()  # Save the changes

        # Return a success response with the updated status
        return Response(
            {
                "message": "Booking has been successfully canceled." ,
                "is_canceled": booking.is_canceled ,
            } ,
            status = status.HTTP_200_OK ,
        )