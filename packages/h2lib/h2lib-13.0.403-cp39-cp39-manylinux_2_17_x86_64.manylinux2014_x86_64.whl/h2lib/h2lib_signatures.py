from h2lib.dll_wrapper import DLLWrapper
class H2LibSignatures():
    def echo_version(self, ):
        '''subroutine echo_version() bind(c, name='echo_version')
!        end subroutine'''
        return self.get_lib_function('echo_version')()

    def getSquare(self, val, restype):
        '''function getsquare(val) result(valsquared) bind(c, name='getsquare')
		!dec$ attributes dllexport :: getsquare
        use, intrinsic :: iso_fortran_env, only: rk => real64
        real(rk), intent(in) :: val
        real(rk)             :: valsquared
        valsquared = val ** 2
    end function'''
        return self.get_lib_function('getSquare')(val, restype=restype)

    def getState(self, restype):
        '''function getstate() result(val) bind(c, name='getstate')
		!dec$ attributes dllexport :: getstate
        integer             :: val
        val = state
    end function'''
        return self.get_lib_function('getState')(restype=restype)

    def get_version(self, s):
        '''subroutine get_version(s) bind(c, name='get_version')
                use iso_c_binding
                implicit none
                character(kind=c_char, len=1), intent(inout)  :: s(255)
            end subroutine'''
        return self.get_lib_function('get_version')(s)

    def setState(self, val):
        '''subroutine setstate(val) bind(c, name='setstate')
		!dec$ attributes dllexport :: setstate
		integer, intent(in) :: val
		state = val
	end subroutine'''
        return self.get_lib_function('setState')(val)

    def sqr2(self, val):
        '''subroutine sqr2(val) bind(c, name='sqr2')
		!dec$ attributes dllexport :: sqr2
		integer, intent(inout) :: val
		val = val ** 2
	end subroutine'''
        return self.get_lib_function('sqr2')(val)

    def test_hdf5(self, ):
        '''subroutine test_hdf5() bind(c, name='test_hdf5')
		!dec$ attributes dllexport :: test_hdf5
		use hdf5
		use iso_c_binding
		
		integer     ::   hdferr ! error flag
		character(9) :: filename = 'test.hdf5'
		integer(hid_t) :: file_id       ! file identifier
		integer(hid_t) :: h5_create_file,h5_open_file      ! file identifier
		type(c_ptr) :: x
		
		print *, "test hdf5"
		print *, "system:", c_sizeof(x) * 8, 'bit'
		
		print *, "create file"
		call h5open_f(hdferr)
		call h5fcreate_f(filename, h5f_acc_trunc_f, file_id, hdferr) !h5f_acc_trunc_f overwrite existing file
		h5_create_file = file_id
		
		print *, "open file"
		call h5fopen_f(filename, h5f_acc_rdwr_f, file_id, hdferr)
		h5_open_file = file_id
		
		print *, "close file"
		call h5fclose_f(file_id, hdferr)
		call h5close_f(hdferr)
		
		print *, "test succeeded"
	end subroutine'''
        return self.get_lib_function('test_hdf5')()

    def test_mkl(self, ):
        '''subroutine test_mkl() bind(c, name='test_mkl')
		!dec$ attributes dllexport :: test_mkl
		use mymkl
		implicit none

		! variables
		
		real(8),dimension(3)::t3, tt3
		real(8),dimension(3,3)::t33

		! body of test_mkl
		print *, 'hello world'
		
		
		call dgemv('n',3,3,1.d0,t33,3,t3,1,0.d0,tt3,1)
		print *, tt3
	 end subroutine'''
        return self.get_lib_function('test_mkl')()
