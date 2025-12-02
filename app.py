from tkinter import *
from tkinterdnd2 import DND_FILES, TkinterDnD
from PyPDF2 import PdfReader
from openAI_interface import LLM_Interact
import threading


dropped_pdf_path = None 
llm = LLM_Interact()

def drop_pdf(event):

    global dropped_pdf_path
    path = event.data.strip()
    
   
    if path.startswith("{") and path.endswith("}"):
        path = path[1:-1]

    if path.lower().endswith(".pdf"):
        dropped_pdf_path = path
        label_message.config(text=f"PDF dropped")
    else: 
        label_message.config(text=f"Only PDFs permitted. Please try again with a PDF file.")
    

def start_qa():
    
    if dropped_pdf_path == None:
        label_message.config(text=f"You need to drop a pdf first before starting the Q&A.")
    else: 
        # check submitted pdf for acceptable lentgh (number of pages)
        reader = PdfReader(dropped_pdf_path)
        num_pages = len(reader.pages)
        if num_pages > 5: 
            label_message.config(text=f"Your pdf is to large ({num_pages} pages). A maximum of 5 pages is allowed.")
        else: 
            # to debug: label_message.config(text=f"PDF accepted! ({num_pages} pages)")
            llm.set_study_notes(dropped_pdf_path)
            show_question_page()
        
def show_question_page():
    
    # hide root page
    for widget in root.winfo_children():
        widget.pack_forget()
    
    # new frame for the question page
    frame_question = Frame(root, bg="#FFB347") # light blue
    frame_question.pack(expand=True, fill=BOTH, padx=(100,40), pady=(30, 0))

    label_question = Label(frame_question, text="Loading ...", font=("Helvetica", 18), wraplength=900, justify=LEFT,  bg="#FFB347")
    label_question.pack(pady=(120,80))
    
    

    # field to enter the answer
    entry_answer = Entry(frame_question, width=70, font=("Helvetica", 18))
    entry_answer.pack(pady=5)
    
    
    # set focus so that the text immediately appers in there and you don't have to click on it bevore typing something
    entry_answer.focus_set()
    
    def worker():
            global question
            question  = llm.get_new_question()
            root.after(0, lambda: label_question.config(text= question))
            
    threading.Thread(target=worker).start()


   
    def on_submit():
        answer = entry_answer.get()
        MAX_CHARS = 300 
        
            
        if len(answer) > MAX_CHARS:
            result_label.config(text="Your answer is too long to check (only 300 chars permitted). Please try a shorter answer.")
            return
        
        
        # show loading sign
        result_label.config(text="Loading...")
         
        def worker():
            result = llm.check_answer(question, answer)
            root.after(0, lambda: result_label.config(text=result))
            
        threading.Thread(target=worker).start()
            
        
    def on_hint():
        # show loading sign 
        hint_label.config(text="Loading ...")
        
        def worker():
            result = llm.get_hint(question)
            root.after(0, lambda: hint_label.config(text=result))
            
        threading.Thread(target=worker).start()
        
    def on_next_question():
        show_question_page()
        
    def on_end():
        show_start_page()
        
    # shortcut to check the answer when pressing enter
    def submit_on_enter(event):
        on_submit() 
    entry_answer.bind("<Return>", submit_on_enter)

    
    # Frame für Hint
    frame_hint = Frame(frame_question, relief="groove", bd=2, padx=10, pady=10, bg="#FFDAB9") # light orange
    frame_hint.pack(pady= (90,0), fill="x")

    btn_hint = Button(frame_hint, text="        Hint        ", command=on_hint, font=("Helvetica", 18), bg="#FFB347")
    btn_hint.pack(side=LEFT, padx=5)

    hint_label = Label(frame_hint, text="", font=("Helvetica", 18), fg="#00008B", wraplength=800, justify=LEFT, bg="#FFDAB9")
    hint_label.pack(side=LEFT, padx=10)
    
    # Frame für Check Answer
    frame_check = Frame(frame_question, relief="groove", bd=2, padx=10, pady=10, bg="#FFDAB9") # light orange
    frame_check.pack(pady=10, fill="x")

    btn_submit = Button(frame_check, text="Check Answer", command=on_submit, font=("Helvetica", 18), bg="#FFB347")
    btn_submit.pack(side=LEFT, padx=5)

    result_label = Label(frame_check, text="", font=("Helvetica", 18), fg="#00008B", wraplength=800, justify=LEFT, bg="#FFDAB9")
    result_label.pack(side=LEFT, padx=10)

    
    # next button
    btn_next = Button(frame_question, text="Next question", command=on_next_question, font=("Helvetica", 18))
    btn_next.pack(pady=100)
    
    # end button
    btn_end = Button(frame_question, text="End Q&A", command=on_end, font=("Helvetica", 18))
    btn_end.place(relx=1.0, y=1, anchor="ne") 

    
    # shortcut to show hint 
    def hint_on_arrow(event):
        on_hint()
    root.bind("<Up>", hint_on_arrow)
    
def show_start_page():
    for widget in root.winfo_children():
        widget.pack_forget()

    label_info.pack(pady=100)
    label_info2.pack(pady=50)
    drop_area.pack(pady=20)
    btn_start.pack(pady=30)
    label_message.pack(pady=10)

    

# Bulid GUI
root = TkinterDnD.Tk()
root.title("Studdy Buddy")
root.geometry("1200x900")
root.configure(bg="#FFB347")  # light orange


# shortcut to show next question 
def next_question_on_arrow(event):
    show_question_page()
root.bind("<Right>", next_question_on_arrow)

label_info = Label(
    root, 
    text=" STUDY BUDDY ", 
    bg="#FFB347",       
    fg="#00008B",        
    font=("Helvetica", 48, "bold") 
)
label_info.pack(pady=100)


label_info2 = Label(root, text="Drag and drop a pdf file with what you want to learn here (lecture slides, summary, ...): ", font=("Helvetica", 18), bg="#FFB347")
label_info2.pack(pady=50)

# Drag & Drop area
drop_area = Label(root, text="⇩ Drop PDF here ⇩", relief="ridge", font=("Helvetica", 18), width=50, height=5, bg="#D37E1E")
drop_area.pack(pady=20)

drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind("<<Drop>>", drop_pdf)

# Start Q&A - Button 
btn_start = Button(root, text="Start Q & A", font=("Helvetica", 18), command=start_qa)
btn_start.pack(pady=30)

# label to sent error if is to long
label_message = Label(root, text="", fg="#00008B", font=("Helvetica", 18), bg="#FFB347")
label_message.pack(pady=10)

root.mainloop()


