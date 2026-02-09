# Overview of Workflow of Program

> Note: This overview may not mention every single detail.

---

## Workflow Steps

1. **HTTP router [main.py]**  
   - Entry point of the workflow.

2. **Create `push_payload` from JSON “file” in HTTP body**  
   - Uses `push_payload.py`.

3. **Call Task Service**  
   - *Not yet created.*  
   - Passes the JSON object.

4. **Create Task object**  
   - Uses `id_service.py`.

5. **Call Task Runner**  
   - Possibly with the Task object.

6. **Create Temporary Folder**  
   - Uses `file_service.py`.

7. **Clone from Git**  
   - Uses `gitclone_service.py`.

8. **Call Pipeline Stage Service**  
   - Executes pipeline stages.  
   - Returns results as a **list of stage results**.

9. **Create TaskResult object**  
   - Uses the list of stage results.

10. **Call Notification Service**  
    - Passes the TaskResult object.

11. **Copy Folder to Logs (later stage — P+ task)**  

12. **Delete Temporary Folder**
