EXPORT inclist := MODULE
    EXPORT rec := RECORD
	INTEGER val;
    END;
    
    EXPORT rec increment(rec in) := TRANSFORM
	self.val := in.val + 1;
    END;
    EXPORT increment_list(set ds) := PROJECT(DATASET(ds, rec), increment(LEFT));
END;

/*

EXPORT inclist(set ints) := MODULE
    EXPORT rec := RECORD
     INTEGER val;
    END;
    SHARED ds := DATASET([1,2,3],rec);
    EXPORT rec increment(rec in) := TRANSFORM
     self.val := in.val + 1;
    END;
    EXPORT increment_list := PROJECT(ds, increment(LEFT));
END;

*/