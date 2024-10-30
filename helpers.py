def fstr(template, objects):
   """
   Allows you to do "delayed templating", i.e. write the template and then evaluate it later. It can run methods attached to the objects passed in.

   Args:
      objects (dict): dict of objects referenced in the template. 
      in the form of {'my_bed': my_bed}, where 'my_bed' is how the object is referenced in the template and my_bed is the actual object.

      Templates must use this 'objects' term, e.g.
         "You are standing at the foot of {objects['my_bed'].getLink('your bed')}"
      So, if you want to change how you refer to it in the templates, you have to change the name of the variable here.
      Does this seem janky? Yes. Is there some way around this? I'm not sure.
   
   Example of usage: 
   ```
   template_a = "You are standing at the foot of {objects['my_bed'].getLink('your bed')}."
   objects = {'my_bed' : my_bed}
   print(fstr(template_a))
   # You are standing at the foot of <a href='object/your-bed'>your bed</a>.
   ```

   Idea taken from user "kadee" on stackoverflow https://stackoverflow.com/a/53671539/25549425
   """
   return eval(f'f"""{template}"""')
