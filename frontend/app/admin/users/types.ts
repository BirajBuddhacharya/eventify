export type User = {
    email: string
    imageUrl: string | undefined
    createdAt: number
    role: string
    fid: string
    branchId?: string
  }
  
  export type CurrentUser = {
    email: string
    imageUrl: string | null
    role: string
    fid: string
  }
  
  export type Branch = {
    branch_id: number
    branch_name: string
  }
  
  export type UserManagementContextType = {
    users: User[]
    setUsers: (users: User[]) => void
    branches: Branch[]
    setBranches: (branches: Branch[]) => void
    currentUser: CurrentUser | null
    setCurrentUser: (user: CurrentUser | null) => void
    isLoading: boolean
    setIsLoading: (loading: boolean) => void
    showBranchDialog: boolean
    setShowBranchDialog: (show: boolean) => void
    selectedUserId: number
    setSelectedUserId: (id: string) => void
    selectedRole: string
    setSelectedRole: (role: string) => void
    branchId: string
    setBranchId: (id: string) => void
    changingRole: string
    setChangingRole: (id: string) => void
    filteredUsers: User[]
    setFilteredUsers: (users: User[]) => void
    setSearchTerm: (query: string) => void
    searchTerm: string
    setIsDeleteUserDialogOpen: (isOpen: boolean) => void
    isDeleteUserDialogOpen: boolean
    handleDelete: (user_id: number) => void
    isAdminRoleChangeDialogOpen: boolean
    setIsAdminRoleChangeDialogOpen: (isOpen: boolean) => void
    changeRole: (user_id: string, new_role: string) => void
  }