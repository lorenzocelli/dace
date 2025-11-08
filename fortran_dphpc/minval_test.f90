PROGRAM run_minval_test
    IMPLICIT NONE
    DOUBLE PRECISION, DIMENSION(2, 2) :: d
    DOUBLE PRECISION, DIMENSION(1) :: res

    ! Initialize some values
    d = RESHAPE((/ 5.0D0, 2.0D0, 8.0D0, -18.0D0 /), SHAPE(d))

    ! Call the subroutine
    CALL minval_test_function(d, res)

    ! Print the result
    PRINT *, 'Minimum value is:', res(1)
END PROGRAM run_minval_test


SUBROUTINE minval_test_function(d, res)
    DOUBLE PRECISION, DIMENSION(2, 2) :: d
    DOUBLE PRECISION, DIMENSION(1) :: res

    res(1) = MINVAL(d)
END SUBROUTINE minval_test_function
