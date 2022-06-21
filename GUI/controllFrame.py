
import  tkinter     as      tk
import  json
import  random

from    Util        import sortTrJsonDataByElement

class ControllFrame(tk.Frame) :
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        for columno in range(0, 7) :
            self.columnconfigure(columno, weight=1)

        self.configure(bg="white", relief="sunken", borderwidth=1)

        self.sortCombines = {"Course Code":False, "Course Name":False, "Course Language":False, "Course ETCS":False, "Course Notation":False, "Course Grade":False, "Course Code":False, "Course Date":False}
        self.lastSortCombine = None

        orderSortButton = tk.Button(self, text="Sort by Date", command=lambda : self.sortData("Course Date"))
        courseCodeSortButton = tk.Button(self, text="Sort by Code", command=lambda : self.sortData("Course Code"))
        courseNameSortButton = tk.Button(self, text="Sort by Name", command=lambda : self.sortData("Course Name"))
        courseLanguageSortButton = tk.Button(self, text="Sort by Language", command=lambda : self.sortData("Course Language"))
        courseEtcsSortButton = tk.Button(self, text="Sort by ETCS", command=lambda : self.sortData("Course ETCS"))
        courseNotationSortButton = tk.Button(self, text="Sort by Notation", command=lambda : self.sortData("Course Notation"))
        courseGradeSortButton = tk.Button(self, text="Sort by Grade", command=lambda : self.sortData("Course Grade"))

        orderSortButton.grid(row=0, column=0, sticky="WE")
        courseCodeSortButton.grid(row=0, column=1, sticky="WE")
        courseNameSortButton.grid(row=0, column=2, sticky="WE")
        courseLanguageSortButton.grid(row=0, column=3, sticky="WE")
        courseEtcsSortButton.grid(row=0, column=4, sticky="WE")
        courseNotationSortButton.grid(row=0, column=5, sticky="WE")
        courseGradeSortButton.grid(row=0, column=6, sticky="WE")

        resetButton = tk.Button(self, text="Reset", command=self.resetData)
        magicButton = tk.Button(self, text="Suprise", command=self.doSomeMagic)
        dummy = tk.Button(self, text="", state="disabled")
        restartButton = tk.Button(self, text="Restart", command=self.root.restartProgram)
        exitButton = tk.Button(self, text="Exit", command = self.root.destroy)

        resetButton.grid(row=1, column=0, columnspan=2, sticky="WE")
        magicButton.grid(row=1, column=2, sticky="WE")
        dummy.grid(row=1, column=3, sticky="WE")
        restartButton.grid(row=1, column=4, sticky="WE")
        exitButton.grid(row=1, column=5, columnspan=2, sticky="WE")

        for label in self.winfo_children():
            label.configure(font=("Segoe UI", 11, "bold"), foreground="black")
            label.grid_configure(padx=1)

    def sortData(self, element, *event) :
        sortTrJsonDataByElement(element, self.sortCombines[element])
        self.sortCombines[element] = not self.sortCombines[element]
        self.lastSortCombine = element
        self.updateData()

    def resetData(self, *event) :
        self.lastSortCombine = None
        with open ("Temp/transcriptDataInit.json", "r", encoding="utf-8") as f :
            with open ("Temp/transcriptData.json", "w", encoding="utf-8") as f2 :
                f2.write(f.read())
        self.updateData()

    def updateData(self, *event) :
        self.root.displaySection.gridCoursesOnCanvas()

    def confirmValues(self, *event) :
        self.root.displaySection.updateCGPA()

    # I knew you were wondering wtf was this method doing. It does nothing. It just used to fills the empty spaces ... (sory)
    def doSomeMagic(self) :
        self.lastSortCombine = None

        luckyNotation = random.choice(self.root.displaySection.possibleNotations)

        with open ("Temp/transcriptData.json", "r", encoding="utf-8") as f :
            data = json.load(f)

        for courseValues in data.values() :
            courseValues[-3] = luckyNotation
            try :
                weight = self.root.displaySection.weights[luckyNotation]
            except KeyError :
                weight = 0
            courseValues[-2] = weight * float(courseValues[-4])

        with open ("Temp/transcriptData.json", "w", encoding="utf-8") as f :
            json.dump(data, f, indent=4)

        self.updateData()