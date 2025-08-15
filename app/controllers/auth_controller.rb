class AuthController < ApplicationController
  def github
    info = request.env["omniauth.auth"]

    Rails.logger.info "GITHUB AUTH PAYLOAD:\n#{info.inspect}"

    puts "Provider: #{info.provider}"
    puts "UID: #{info.uid}"
    puts "Login: #{info.info&.nickname}"
    puts "Email: #{info.info&.email}"
    puts "Avatar: #{info.info&.image}"

    render json: {
      ok: true,
      provider: info.provider,
      uid: info.uid,
      login: info.info&.nickname,
      email: info.info&.email,
      avatar_url: info.info&.image
    }
  end

  def failure
    render json: { ok: false, error: params[:message] }, status: :unauthorized
  end
end
