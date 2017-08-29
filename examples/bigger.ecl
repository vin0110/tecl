EXPORT bigger := MODULE
    EXPORT rec := RECORD
	INTEGER val;
    END;

    EXPORT bigger(set ints, integer c) := DATASET(ints, rec)(val > c);
END;

