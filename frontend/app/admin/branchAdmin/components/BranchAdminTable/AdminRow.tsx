'use client'

import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { BranchAdmin } from "../../types"
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { ChevronDown } from 'lucide-react'
import { useBranchAdmin } from "../../context"
import { useAuth } from '@/context/auth/hooks'
import { toast } from 'react-toastify'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'

const AdminRow = ({
  admin,
  onChangeBranch,
  index,
}: {
  admin: BranchAdmin
  onChangeBranch: (value: boolean) => void
  index: number
}) => (
  <motion.tr
    key={admin.user_id}
    className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: index * 0.1 }}
  >
    <td className="p-4 align-middle font-medium flex gap-3 items-center">
      <Avatar className="h-8 w-8">
        <AvatarImage src={admin.imageUrl} />
        <AvatarFallback>{admin.email[0].toUpperCase()}</AvatarFallback>
      </Avatar>
      {admin.email}
    </td>
    <td className="p-4 align-middle">{admin.branch_name}</td>
    <td className="p-4 align-middle">{admin.location}</td>
    <td className="p-4 align-middle w-full flex justify-center">
      <AdminActions userId={admin.user_id} onChangeBranch={onChangeBranch} />
    </td>
  </motion.tr>
)

const AdminActions = ({ userId, onChangeBranch }: { userId: string; onChangeBranch: (value: boolean) => void }) => {
  const { setSelectedUserId, handleBranchAdminDelete, isDeleting } = useBranchAdmin()
  const { axiosInstance } = useAuth()

  const handleBranchChange = () => {
    setSelectedUserId(userId)
    onChangeBranch(true)
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="sm" disabled={isDeleting}>
          Actions
          <ChevronDown className="ml-2 h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={handleBranchChange}>Change Branch</DropdownMenuItem>
        <DropdownMenuItem
          className="text-red-600"
          onClick={() => handleBranchAdminDelete(userId)}
          disabled={isDeleting}
        >
          {isDeleting ? 'Demoting...' : 'Demote User'}
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

export default AdminRow