# HL7 Listener

`server.py` contains a http server that listen to HL7 messages. It will only listen to Outpatient MRI messages and update status of corresponding studies. It stores the studies status in a mongo Docker container.

Make sure this component is running all the time. When you first run this component, hit it with the HL7 messages for last two weeks to bootstrap it.
