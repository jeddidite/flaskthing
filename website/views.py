from flask import request
from flask import Blueprint, render_template

views = Blueprint('views', __name__ ) #Initiates Blueprint for file structure 

@views.route('/') #Initiates filestructure to be seperated via '/'

# Home Page IE https://charliescomputerlab.com/
def home():
    return "<h1>Test</h1>"

@views.route('/get_appointments', methods=['POST'])
def get_appointments():
    # Get the selected technician from the request data
    technician = request.form.get('technician')

    # Get the appointments for the selected technician
    # This depends on how you're storing and accessing your appointments
    appointments = get_appointments_for_technician(technician)

    # Convert the appointments to a string or HTML
    # This depends on what format you want to send back
    appointments_html = convert_appointments_to_html(appointments)

    # Return the appointments
    return appointments_html

@views.route('/calander')
def calander():
    from datetime import datetime, timedelta
    from collections import defaultdict

    # Define technicians and their working hours
    technicians = ['Kevin', 'Jule', 'Mini-Mouse', 'Manwell']
    working_hours = (12, 19)  # 12:00 PM to 7:00 PM in 24-hour format

    # Data structure to hold appointments
    appointments = defaultdict(list)

    def is_available(technician, start_time, service_type):
       if technician not in technicians:
           return False
       if not (working_hours[0] <= start_time.hour < working_hours[1]):
           return False
       for appointment in appointments[technician]:
           if start_time == appointment['start_time']:
               return False # Technician is not available at this time
       manicure_count = 0
       for appointment in appointments[technician]:
           if appointment['service_type'] == 'manicure':
               manicure_count += 1
       if service_type == 'manicure' and manicure_count >= 2:
           return False # Can't schedule more than 2 manicures in the same hour
       return True

    def schedule_appointment(technician, service_type):
      service_types = {1: 'manicure', 2: 'pedicure'}
      if service_type not in service_types.values():
          return "Invalid service type."
      available_times = []
      for hour in range(working_hours[0], working_hours[1]):
          for minute in range(60):
              start_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, hour, minute)
              if is_available(technician, start_time, service_type):
                  available_times.append(start_time)
      if not available_times:
          return "No available times for this service type."
      selected_time = min(available_times)
      end_time = selected_time + timedelta(hours=1)
      appointments[technician].append({
          'start_time': selected_time,
          'end_time': end_time,
          'service_type': service_type
      })
      return f"Appointment scheduled successfully at {selected_time.strftime('%H:%M')}."

    def print_available_times(technician, service_type):
      available_times = []
      for hour in range(working_hours[0], working_hours[1]):
          start_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, hour, 0)
          if is_available(technician, start_time, service_type):
              available_times.append(start_time)
      print(f"Available times for {service_type}s:")
      for time in available_times:
          print(time.strftime("%H:%M"))

    def choose_technician():
       print("Choose a technician:")
       for index, technician in enumerate(technicians, start=1):
           print(f"{index}. {technician}")
       choice = input("Enter the number of the technician: ")
       try:
           choice = int(choice) - 1
           if 0 <= choice < len(technicians):
               chosen_technician = technicians[choice]
               print_available_times(chosen_technician, 'manicure')
               return chosen_technician
           else:
               print("Invalid choice. Please choose a valid technician number.")
               return None
       except ValueError:
           print("Invalid input. Please enter a number.")
           return None

    def choose_service_type():
        service_types = {1: 'manicure', 2: 'pedicure'}
        print("Choose a service type:")
        for option, service in service_types.items():
            print(f"{option}. {service}")
        choice = input("Enter the number of the service type: ")
        try:
            choice = int(choice)
            if choice in service_types:
                return service_types[choice]
            else:
                print("Invalid choice. Please choose a valid service type number.")
                return None
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None

    def main():
        while True:
            print("\nScheduler CLI")
            print("1. Schedule an appointment")
            print("2. Exit")
            choice = input("Enter your choice: ")
        
            if choice == "1":
                technician = choose_technician()
                if technician is None:
                    continue
                service_type = choose_service_type()
                if service_type is None:
                    continue
                appointment_time = input("Enter appointment time (HH:MM): ")
            
                try:
                    appointment_time = datetime.strptime(appointment_time, "%H:%M").replace(
                        year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
                    )
                    result = schedule_appointment(technician, appointment_time, service_type)
                    print(result)
                except ValueError:
                    print("Invalid time format. Please use HH:MM.")
            elif choice == "2":
                break
            else:
                print("Invalid choice. Please try again.")

    if __name__ == "__main__":
        main()
    data = {
        'technicians': technicians,
        'appointments': appointments,
        # Add other data you want to display here
    }

    # Render the template and pass the data to it
    return render_template('calendar.html', **data)
