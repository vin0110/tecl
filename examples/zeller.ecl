// zeller's algorithm
// https://en.wikipedia.org/wiki/Zeller%27s_congruence
EXPORT zeller := MODULE
    zeller_(INTEGER k, INTEGER j, INTEGER m, INTEGER d) :=
      (d + (13 * m)/5 + k + k DIV 4 + j DIV 4 + 5*j) % 7;

    EXPORT zeller(INTEGER year, INTEGER month, INTEGER day) :=
      IF (month < 3,
          zeller_((year-1)%100, (year-1) DIV 100, month+13, day),
          zeller_(year%100, year DIV 100, month+1, day));
END;
