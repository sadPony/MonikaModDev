#Dict holding seen poems and amount of times seen
#poem_id:shown_count
default persistent._mas_poems_seen = dict()

init python in mas_poems:
    poem_map = dict()

init 11 python in mas_poems:
    import store

    def getPoemsByCategory(category, unseen=False):
        """
        Returns a list of poems by the category provided
        """

        #If we only want unseen, do this
        if unseen:
            return [
                poem
                for poem in poem_map.itervalues()
                if not poem.is_seen() and poem.category == category
            ]

        #Otherwise we just get all
        return [
            poem
            for poem in poem_map.itervalues()
            if poem.category == category
        ]

    def getSeenPoems():
        """
        Returns a list of all seen poems
        """
        return [
            poem
            for poem in poem_map.itervalues()
            if poem.is_seen()
        ]

    def getUnseenPoems():
        """
        Returns a list of all unseen poems
        """
        return [
            poem
            for poem in poem_map.itervalues()
            if not poem.is_seen()
        ]

    def getPoem(poem_id):
        """
        Gets a poem by id

        IN:
            poem_id - poem id of the poem to get

        OUT:
            MASPoem if there's a poem with the id
            None if no poem with the id exists
        """
        return poem_map.get(poem_id, None)

init 10 python:
    class MASPoem:
        def __init__(
            self,
            poem_id,
            category,
            title="",
            text="",
            author="monika"
        ):
            """
            MASPoem constructor

            Similar to the Poem class from DDLC, but excludes the yuri variables and adds a poem id property.


            poem_id:
                identifier for the poem. (NOTE: Must be unique)

            category:
                category for the poem is under (So we can get poems by category)

            title:
                poem title (supports renpy substitution)

            text:
                poem contents

            author:
                poem author (Default: monika)
            """
            if poem_id in store.mas_poems.poem_map:
                raise Exception ("poem_id {0} already exists in the poem map.".format(poem_id))

            self.poem_id=poem_id
            self.category=category
            self.title=renpy.substitute(title)
            self.text=text
            self.author=author

            #And add this to map
            store.mas_poems.poem_map[poem_id] = self

        def is_seen(self):
            """
            Checks if the poem is seen

            OUT:
                boolean:
                    - True if poem was seen before
                    - False otherwise
            """
            return self.poem_id in store.persistent._mas_poems_seen

        def get_shown_count(self):
            """
            Gets the shown count of the poem

            OUT:
                integer:
                    - The amount of times this poem was seen
            """
            return store.persistent._mas_poems_seen.get(self.poem_id, 0)


label mas_showpoem(poem=None, paper=None):
    if poem == None:
        return

    play sound page_turn

    window hide
    $ renpy.game.preferences.afm_enable = False

    if paper:
        show screen poem(poem, paper=paper)
    else:
        show screen poem(poem)

    with Dissolve(1)

    $ pause()

    hide screen poem
    with Dissolve(.5)
    window auto

    #Flag this poem as seen
    if poem.poem_id in persistent._mas_poems_seen:
        $ persistent._mas_poems_seen[poem.poem_id] += 1
    else:
        $ persistent._mas_poems_seen[poem.poem_id] = 1
    return
